/**
 * File Uploader Component for Admin Ingestion
 *
 * Drag-and-drop file upload with progress tracking.
 */

import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { useAuth } from '@site/src/hooks/useAuth';

// API base URL — SSR-safe: window not available during static generation
const API_BASE_URL = process.env.NODE_ENV === 'production'
  ? (typeof window !== 'undefined' ? window.location.origin : '')
  : 'https://mb-murad-physical-ai-backend.hf.space';

/**
 * FileUploader component props
 */
interface FileUploaderProps {
  onUploadComplete?: (result: any) => void;
  onUploadError?: (error: Error) => void;
  maxFiles?: number;
  maxSizeMB?: number;
}

/**
 * Upload status for individual files
 */
interface UploadStatus {
  file: File;
  status: 'pending' | 'uploading' | 'success' | 'error';
  progress: number;
  error?: string;
  result?: any;
}

export default function FileUploader({
  onUploadComplete,
  onUploadError,
  maxFiles = 10,
  maxSizeMB = 10,
}: FileUploaderProps) {
  const { user } = useAuth();
  const [uploads, setUploads] = useState<UploadStatus[]>([]);
  const [isDragging, setIsDragging] = useState(false);

  /**
   * Upload a single file with progress tracking
   */
  const uploadFile = async (file: File): Promise<{ success: boolean; result?: any; error?: string }> => {
    return new Promise((resolve) => {
      const xhr = new XMLHttpRequest();
      const formData = new FormData();
      formData.append('file', file);

      // Track upload progress
      xhr.upload.addEventListener('progress', (e) => {
        if (e.lengthComputable) {
          const percentComplete = (e.loaded / e.total) * 100;
          setUploads((prev) =>
            prev.map((u) =>
              u.file === file ? { ...u, progress: percentComplete } : u
            )
          );
        }
      });

      // Handle upload completion
      xhr.addEventListener('load', () => {
        if (xhr.status === 200 || xhr.status === 201) {
          const result = JSON.parse(xhr.responseText);
          resolve({ success: true, result });
        } else {
          let errorMessage = 'Upload failed';
          try {
            const errorData = JSON.parse(xhr.responseText);
            errorMessage = errorData.detail?.message || errorData.message || errorMessage;
          } catch (e) {
            // Ignore parse errors
          }
          resolve({ success: false, error: errorMessage });
        }
      });

      // Handle upload error
      xhr.addEventListener('error', () => {
        resolve({ success: false, error: 'Network error occurred' });
      });

      // Start upload
      xhr.open('POST', `${API_BASE_URL}/api/admin/ingest/upload`);
      xhr.setRequestHeader('Authorization', `Bearer ${localStorage.getItem('access_token')}`);
      xhr.send(formData);
    });
  };

  /**
   * Handle file drop
   */
  const onDrop = useCallback(async (acceptedFiles: File[], rejectedFiles: any[]) => {
    // Process rejected files
    const newUploads: UploadStatus[] = [
      ...rejectedFiles.map((r: any) => ({
        file: r.file,
        status: 'error' as const,
        progress: 0,
        error: r.errors[0]?.message || 'File rejected',
      })),
      ...acceptedFiles.map((file) => ({
        file,
        status: 'pending' as const,
        progress: 0,
      })),
    ];

    setUploads((prev) => [...prev, ...newUploads]);

    // Upload accepted files
    for (const upload of newUploads.filter((u) => u.status === 'pending')) {
      // Update status to uploading
      setUploads((prev) =>
        prev.map((u) =>
          u.file === upload.file ? { ...u, status: 'uploading' } : u
        )
      );

      // Perform upload
      const result = await uploadFile(upload.file);

      // Update status based on result
      setUploads((prev) =>
        prev.map((u) =>
          u.file === upload.file
            ? {
                ...u,
                status: result.success ? 'success' : 'error',
                progress: result.success ? 100 : u.progress,
                result: result.result,
                error: result.error,
              }
            : u
        )
      );

      // Notify parent component
      if (result.success) {
        onUploadComplete?.(result.result);
      } else {
        onUploadError?.(new Error(result.error));
      }
    }
  }, [onUploadComplete, onUploadError]);

  /**
   * Configure dropzone
   */
  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    onDragEnter: () => setIsDragging(true),
    onDragLeave: () => setIsDragging(false),
    onDropAccepted: () => setIsDragging(false),
    onDropRejected: () => setIsDragging(false),
    accept: {
      'application/pdf': ['.pdf'],
      'text/markdown': ['.md'],
      'text/plain': ['.txt'],
    },
    maxFiles,
    maxSize: maxSizeMB * 1024 * 1024,
    disabled: !user?.is_admin,
  });

  /**
   * Clear all uploads
   */
  const clearUploads = () => {
    setUploads([]);
  };

  return (
    <div className="margin-vert--md">
      {/* Dropzone */}
      <div
        {...getRootProps()}
        className={`
          border-2 border-dashed rounded-lg p-8 text-center cursor-pointer
          transition-all duration-200
          ${isDragActive 
            ? 'border-cyan-500 bg-cyan-500/10 scale-105' 
            : 'border-gray-300 hover:border-cyan-400 hover:bg-gray-50'
          }
          ${!user?.is_admin ? 'opacity-50 cursor-not-allowed' : ''}
        `}
        style={{
          background: 'linear-gradient(135deg, rgba(6,182,212,0.05) 0%, rgba(8,145,178,0.05) 100%)',
          backdropFilter: 'blur(10px)',
          border: '1px solid rgba(6,182,212,0.2)',
        }}
      >
        <input {...getInputProps()} />
        
        <div className="space-y-4">
          {/* Icon */}
          <div className="text-6xl">📁</div>
          
          {/* Instructions */}
          {isDragActive ? (
            <p className="text-lg font-semibold text-cyan-600">
              Drop files here to upload...
            </p>
          ) : (
            <div>
              <p className="text-lg font-medium text-gray-700">
                Drag & drop PDF or Markdown files here
              </p>
              <p className="text-sm text-gray-500 margin-top--sm">
                or click to select (max {maxFiles} files, {maxSizeMB}MB each)
              </p>
            </div>
          )}

          {/* Admin warning */}
          {!user?.is_admin && (
            <p className="text-sm text-red-600 font-medium">
              ⚠️ Admin access required to upload files
            </p>
          )}
        </div>
      </div>

      {/* Upload Status */}
      {uploads.length > 0 && (
        <div className="margin-top--md">
          <div className="flex justify-between items-center margin-bottom--sm">
            <h4 className="text-lg font-semibold">Upload Status</h4>
            <button
              onClick={clearUploads}
              className="button button--sm button--outline button--secondary"
            >
              Clear All
            </button>
          </div>

          <div className="space-y-2">
            {uploads.map((upload, index) => (
              <div
                key={`${upload.file.name}-${index}`}
                className="border rounded-md p-3 bg-white shadow-sm"
              >
                <div className="flex justify-between items-start">
                  <div className="flex-1">
                    <p className="font-medium text-sm">{upload.file.name}</p>
                    <p className="text-xs text-gray-500">
                      {(upload.file.size / 1024).toFixed(1)} KB
                    </p>
                  </div>
                  
                  <div className="ml-4">
                    {upload.status === 'pending' && (
                      <span className="badge badge--secondary">Pending</span>
                    )}
                    {upload.status === 'uploading' && (
                      <span className="badge badge--info">Uploading...</span>
                    )}
                    {upload.status === 'success' && (
                      <span className="badge badge--success">✓ Success</span>
                    )}
                    {upload.status === 'error' && (
                      <span className="badge badge--danger">✗ Error</span>
                    )}
                  </div>
                </div>

                {/* Progress Bar */}
                {upload.status === 'uploading' && (
                  <div className="margin-top--sm">
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div
                        className="bg-cyan-500 h-2 rounded-full transition-all duration-300"
                        style={{ width: `${upload.progress}%` }}
                      />
                    </div>
                    <p className="text-xs text-gray-500 margin-top--xs">
                      {upload.progress.toFixed(0)}%
                    </p>
                  </div>
                )}

                {/* Error Message */}
                {upload.status === 'error' && upload.error && (
                  <p className="text-xs text-red-600 margin-top--xs">
                    {upload.error}
                  </p>
                )}

                {/* Success Message */}
                {upload.status === 'success' && upload.result && (
                  <p className="text-xs text-green-600 margin-top--xs">
                    ✓ {upload.result.message || 'Upload successful'}
                  </p>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
