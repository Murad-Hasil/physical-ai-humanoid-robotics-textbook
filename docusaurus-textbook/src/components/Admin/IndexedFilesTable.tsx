/**
 * Indexed Files Table Component
 *
 * Displays list of indexed files with status and metadata.
 */

import React, { useState, useEffect, useCallback } from 'react';
import { useAuth } from '@site/src/hooks/useAuth';

const API_BASE_URL = 'https://mb-murad-physical-ai-backend.hf.space';

interface IndexedFile {
  id: string;
  file_name: string;
  file_size: number;
  file_type: string;
  status: 'pending' | 'processing' | 'completed' | 'failed';
  chunk_count?: number;
  uploaded_by?: {
    id: string;
    email: string;
  };
  uploaded_at?: string;
  indexed_at?: string;
}

interface IndexedFilesTableProps {
  onFileDeleted?: (fileId: string) => void;
  onReindex?: () => void;
}

export default function IndexedFilesTable({
  onFileDeleted,
  onReindex,
}: IndexedFilesTableProps) {
  const { user } = useAuth();
  const [files, setFiles] = useState<IndexedFile[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [total, setTotal] = useState(0);
  const [limit] = useState(50);
  const [offset, setOffset] = useState(0);

  /**
   * Fetch indexed files
   */
  const fetchFiles = useCallback(async () => {
    if (!user?.is_admin) return;

    try {
      setLoading(true);
      setError(null);

      const response = await fetch(
        `${API_BASE_URL}/api/admin/ingest/files?limit=${limit}&offset=${offset}`,
        {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
          },
        }
      );

      if (!response.ok) {
        throw new Error('Failed to fetch files');
      }

      const data = await response.json();
      setFiles(data.files);
      setTotal(data.total);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, [user, limit, offset]);

  /**
   * Auto-refresh every 30 seconds
   */
  useEffect(() => {
    fetchFiles();
    const interval = setInterval(fetchFiles, 30000);
    return () => clearInterval(interval);
  }, [fetchFiles]);

  /**
   * Delete a file
   */
  const handleDelete = async (fileId: string, fileName: string) => {
    if (!confirm(`Are you sure you want to delete "${fileName}"?`)) {
      return;
    }

    try {
      const response = await fetch(
        `${API_BASE_URL}/api/admin/ingest/files/${fileId}`,
        {
          method: 'DELETE',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
          },
        }
      );

      if (!response.ok) {
        throw new Error('Failed to delete file');
      }

      onFileDeleted?.(fileId);
      fetchFiles(); // Refresh list
      
      alert(`✓ "${fileName}" deleted successfully`);
    } catch (err: any) {
      alert(`✗ Error: ${err.message}`);
    }
  };

  /**
   * Format file size
   */
  const formatFileSize = (bytes: number): string => {
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(2)} MB`;
  };

  /**
   * Format date
   */
  const formatDate = (dateString?: string): string => {
    if (!dateString) return 'N/A';
    return new Date(dateString).toLocaleString();
  };

  /**
   * Get status badge class
   */
  const getStatusBadgeClass = (status: string): string => {
    switch (status) {
      case 'completed':
        return 'badge--success';
      case 'processing':
        return 'badge--info';
      case 'pending':
        return 'badge--secondary';
      case 'failed':
        return 'badge--danger';
      default:
        return 'badge--secondary';
    }
  };

  /**
   * Get file type icon
   */
  const getFileTypeIcon = (fileType: string): string => {
    if (fileType.includes('pdf')) return '📄';
    if (fileType.includes('markdown')) return '📝';
    if (fileType.includes('plain')) return '📃';
    return '📁';
  };

  if (!user?.is_admin) {
    return (
      <div className="alert alert--warning margin-vert--md">
        <p>⚠️ Admin access required to view indexed files</p>
      </div>
    );
  }

  if (loading && files.length === 0) {
    return (
      <div className="container margin-vert--xl text--center">
        <div className="spinner spinner--lg"></div>
        <p className="margin-top--md">Loading indexed files...</p>
      </div>
    );
  }

  if (error && files.length === 0) {
    return (
      <div className="alert alert--danger margin-vert--md">
        <p>✗ Error loading files: {error}</p>
        <button
          className="button button--sm button--outline margin-top--sm"
          onClick={fetchFiles}
        >
          Retry
        </button>
      </div>
    );
  }

  return (
    <div className="margin-vert--md">
      {/* Header */}
      <div className="flex justify-between items-center margin-bottom--md">
        <h3 className="text-xl font-bold">
          Indexed Files ({total} total)
        </h3>
        <button
          className="button button--sm button--outline button--primary"
          onClick={fetchFiles}
        >
          🔄 Refresh
        </button>
      </div>

      {/* Table */}
      <div className="table-container">
        <table className="table">
          <thead>
            <tr>
              <th style={{ width: '40%' }}>File Name</th>
              <th style={{ width: '15%' }}>Type</th>
              <th style={{ width: '15%' }}>Size</th>
              <th style={{ width: '10%' }}>Chunks</th>
              <th style={{ width: '10%' }}>Status</th>
              <th style={{ width: '10%' }}>Actions</th>
            </tr>
          </thead>
          <tbody>
            {files.map((file) => (
              <tr key={file.id}>
                <td>
                  <div className="flex items-center">
                    <span className="margin-right--sm">
                      {getFileTypeIcon(file.file_type)}
                    </span>
                    <div>
                      <p className="font-medium text-sm">{file.file_name}</p>
                      <p className="text-xs text-gray-500">
                        Uploaded: {formatDate(file.uploaded_at)}
                      </p>
                    </div>
                  </div>
                </td>
                <td>
                  <span className="text-xs text-gray-600">
                    {file.file_type.split('/')[1]?.toUpperCase() || 'Unknown'}
                  </span>
                </td>
                <td>
                  <span className="text-xs">
                    {formatFileSize(file.file_size)}
                  </span>
                </td>
                <td>
                  <span className="text-xs">
                    {file.chunk_count || 'N/A'}
                  </span>
                </td>
                <td>
                  <span className={`badge ${getStatusBadgeClass(file.status)}`}>
                    {file.status}
                  </span>
                </td>
                <td>
                  <button
                    className="button button--sm button--danger button--outline"
                    onClick={() => handleDelete(file.id, file.file_name)}
                    title="Delete file"
                  >
                    🗑️
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Empty State */}
      {files.length === 0 && (
        <div className="alert alert--info margin-vert--md text--center">
          <p>📭 No files indexed yet</p>
          <p className="text-sm margin-top--sm">
            Upload PDF or Markdown files to get started
          </p>
        </div>
      )}

      {/* Pagination */}
      {files.length > 0 && (
        <div className="flex justify-between items-center margin-top--md">
          <p className="text-sm text-gray-600">
            Showing {offset + 1} - {Math.min(offset + files.length, total)} of {total}
          </p>
          <div className="space-x--sm">
            <button
              className="button button--sm button--outline"
              onClick={() => setOffset(Math.max(0, offset - limit))}
              disabled={offset === 0}
            >
              ← Previous
            </button>
            <button
              className="button button--sm button--outline"
              onClick={() => setOffset(offset + limit)}
              disabled={offset + files.length >= total}
            >
              Next →
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
