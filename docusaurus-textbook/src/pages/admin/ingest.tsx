/**
 * Admin Ingestion Dashboard
 *
 * Protected page for managing RAG knowledge base.
 */

import React, { useState } from 'react';
import Layout from '@theme/Layout';
import { useAuth } from '@site/src/hooks/useAuth';
import AdminGuard from '@site/src/components/AuthGuard';
import FileUploader from '@site/src/components/Admin/FileUploader';
import IndexedFilesTable from '@site/src/components/Admin/IndexedFilesTable';

export default function AdminIngestPage() {
  const { user } = useAuth();
  const [uploadCount, setUploadCount] = useState(0);

  /**
   * Handle upload complete
   */
  const handleUploadComplete = (result: any) => {
    setUploadCount((prev) => prev + 1);
    console.log('Upload complete:', result);
  };

  /**
   * Handle upload error
   */
  const handleUploadError = (error: Error) => {
    console.error('Upload error:', error);
  };

  /**
   * Handle file deleted
   */
  const handleFileDeleted = (fileId: string) => {
    console.log('File deleted:', fileId);
  };

  return (
    <Layout
      title="Admin - Knowledge Base Management"
      description="Manage RAG knowledge base - upload and index files"
    >
      <AdminGuard>
        <div className="container margin-vert--lg">
          {/* Navigation Tabs */}
          <div className="margin-bottom--lg">
            <div className="row">
              <div className="col col--6">
                <a
                  href="/physical-ai-humanoid-robotics-textbook/admin/ingest"
                  className="button button--primary button--lg margin-right--md"
                >
                  📤 Knowledge Base
                </a>
                <a
                  href="/physical-ai-humanoid-robotics-textbook/admin/status"
                  className="button button--secondary button--lg"
                >
                  🛡️ System Status
                </a>
              </div>
            </div>
          </div>

          {/* Header */}
          <div className="margin-bottom--xl">
            <h1 className="text-3xl font-bold" style={{ color: '#ff6b35' }}>
              🛡️ Admin Ingestion Dashboard
            </h1>
            <p className="text-lg text-gray-600 margin-top--sm">
              Manage knowledge base - upload, index, and monitor your RAG content
            </p>
            {user && (
              <p className="text-sm text-gray-500 margin-top--sm">
                Logged in as: <span className="font-medium">{user.email}</span>
              </p>
            )}
          </div>

          {/* Upload Section */}
          <section className="margin-bottom--xl">
            <div
              className="card shadow--md"
              style={{
                background: 'linear-gradient(135deg, rgba(255,107,53,0.05) 0%, rgba(255,154,113,0.05) 100%)',
                border: '1px solid rgba(255,107,53,0.2)',
              }}
            >
              <div className="card__header">
                <h2 className="text-xl font-bold" style={{ color: '#ff6b35' }}>
                  📤 Upload Files
                </h2>
                <p className="text-sm text-gray-600 margin-top--xs">
                  Upload PDF or Markdown files to index in the knowledge base
                </p>
              </div>
              <div className="card__body">
                <FileUploader
                  onUploadComplete={handleUploadComplete}
                  onUploadError={handleUploadError}
                  maxFiles={10}
                  maxSizeMB={10}
                />
                
                {uploadCount > 0 && (
                  <div className="alert alert--success margin-top--md">
                    <p>
                      ✓ Knowledge Base Updated: {uploadCount} file{uploadCount > 1 ? 's' : ''} uploaded successfully
                    </p>
                  </div>
                )}
              </div>
            </div>
          </section>

          {/* Indexed Files Section */}
          <section>
            <div
              className="card shadow--md"
              style={{
                background: 'linear-gradient(135deg, rgba(6,182,212,0.05) 0%, rgba(8,145,178,0.05) 100%)',
                border: '1px solid rgba(6,182,212,0.15)',
              }}
            >
              <div className="card__header">
                <h2 className="text-xl font-bold" style={{ color: '#06b6d4' }}>
                  📚 Indexed Files
                </h2>
                <p className="text-sm text-gray-600 margin-top--xs">
                  View and manage all indexed documents in the knowledge base
                </p>
              </div>
              <div className="card__body">
                <IndexedFilesTable
                  onFileDeleted={handleFileDeleted}
                />
              </div>
            </div>
          </section>

          {/* Info Section */}
          <section className="margin-top--xl">
            <div className="alert alert--info">
              <h4 className="alert__heading">ℹ️ Information</h4>
              <ul className="margin-top--sm">
                <li>Maximum file size: 10MB per file</li>
                <li>Maximum batch upload: 10 files at once</li>
                <li>Supported formats: PDF, Markdown (.md), Text (.txt)</li>
                <li>Files are automatically indexed and become searchable immediately</li>
                <li>Only admin users can access this page</li>
              </ul>
            </div>
          </section>
        </div>
      </AdminGuard>
    </Layout>
  );
}
