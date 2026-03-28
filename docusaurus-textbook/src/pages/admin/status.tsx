/**
 * Admin System Status Dashboard
 *
 * Protected page for monitoring system health, performance metrics, and re-indexing.
 */

import React, { useState, useEffect } from 'react';
import Layout from '@theme/Layout';
import { useAuth } from '@site/src/hooks/useAuth';
import AdminGuard from '@site/src/components/AuthGuard';
import HealthCard from '@site/src/components/Admin/HealthCard';

interface HealthService {
  status: 'healthy' | 'unhealthy' | 'degraded';
  response_time_ms: number;
  error?: string;
  last_checked?: string;
  collection?: string;
  document_count?: number;
  endpoint?: string;
}

interface HealthData {
  services: {
    postgresql: HealthService;
    qdrant: HealthService;
    grok_api: HealthService;
  };
  overall_status: string;
  timestamp: string;
}

interface StatsData {
  rag_latency: {
    avg_ms: number;
    p95_ms: number;
    p99_ms: number;
    sample_count: number;
    time_range: string;
  };
  llm_latency: {
    avg_ms: number;
    p95_ms: number;
    p99_ms: number;
    sample_count: number;
    time_range: string;
  };
  usage_analytics: {
    total_queries: number;
    total_tokens: number;
    unique_users: number;
    time_range: string;
  };
  last_updated: string;
}

interface ReindexStatus {
  status: 'idle' | 'queued' | 'running' | 'completed' | 'failed';
  job_id?: string;
  progress?: {
    processed_files: number;
    total_files: number;
    failed_files: number;
    percent_complete: number;
  };
  current_file?: string | null;
  timing?: {
    started_at?: string;
    completed_at?: string;
    elapsed_seconds: number;
    estimated_remaining_seconds: number;
  };
}

export default function AdminSystemStatusPage() {
  const { user } = useAuth();
  
  // State
  const [healthData, setHealthData] = useState<HealthData | null>(null);
  const [statsData, setStatsData] = useState<StatsData | null>(null);
  const [reindexStatus, setReindexStatus] = useState<ReindexStatus>({ status: 'idle' });
  const [loading, setLoading] = useState(true);
  const [reindexing, setReindexing] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // API base URL — Docusaurus uses Webpack, not Vite; env vars not polyfilled at runtime
  const API_URL = 'https://mb-murad-physical-ai-backend.hf.space';

  /**
   * Fetch health data
   */
  const fetchHealth = async () => {
    try {
      const token = localStorage.getItem('access_token');
      const response = await fetch(`${API_URL}/api/admin/health`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        throw new Error('Failed to fetch health data');
      }

      const data = await response.json();
      setHealthData(data);
    } catch (err) {
      console.error('Health fetch error:', err);
      setError('Failed to load health data');
    }
  };

  /**
   * Fetch stats data
   */
  const fetchStats = async () => {
    try {
      const token = localStorage.getItem('access_token');
      const response = await fetch(`${API_URL}/api/admin/stats?time_range=1h`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        throw new Error('Failed to fetch stats data');
      }

      const data = await response.json();
      setStatsData(data);
    } catch (err) {
      console.error('Stats fetch error:', err);
      setError('Failed to load stats data');
    }
  };

  /**
   * Fetch reindex status
   */
  const fetchReindexStatus = async () => {
    try {
      const token = localStorage.getItem('access_token');
      const response = await fetch(`${API_URL}/api/admin/ingest/reindex/status`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        throw new Error('Failed to fetch reindex status');
      }

      const data = await response.json();
      setReindexStatus(data);
      
      // Check if reindexing is complete
      if (data.status === 'completed' || data.status === 'failed' || data.status === 'idle') {
        setReindexing(false);
      }
    } catch (err) {
      console.error('Reindex status error:', err);
    }
  };

  /**
   * Trigger re-indexing
   */
  const handleTriggerReindex = async () => {
    if (!confirm('Are you sure you want to re-index all files? This may take several minutes.')) {
      return;
    }

    try {
      setReindexing(true);
      setError(null);

      const token = localStorage.getItem('access_token');
      const response = await fetch(`${API_URL}/api/admin/ingest/reindex`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail?.message || 'Failed to start re-indexing');
      }

      const data = await response.json();
      console.log('Re-indexing started:', data);
      
      // Start polling for status
      const pollInterval = setInterval(fetchReindexStatus, 5000);
      
      // Stop polling after 10 minutes
      setTimeout(() => {
        clearInterval(pollInterval);
      }, 600000);

    } catch (err: any) {
      console.error('Reindex error:', err);
      setError(err.message);
      setReindexing(false);
    }
  };

  /**
   * Load initial data
   */
  useEffect(() => {
    const loadData = async () => {
      setLoading(true);
      await Promise.all([fetchHealth(), fetchStats(), fetchReindexStatus()]);
      setLoading(false);
    };

    loadData();

    // Refresh health every 30 seconds
    const healthInterval = setInterval(fetchHealth, 30000);
    
    // Refresh stats every 60 seconds
    const statsInterval = setInterval(fetchStats, 60000);
    
    // Refresh reindex status every 5 seconds
    const reindexInterval = setInterval(fetchReindexStatus, 5000);

    return () => {
      clearInterval(healthInterval);
      clearInterval(statsInterval);
      clearInterval(reindexInterval);
    };
  }, []);

  /**
   * Get knowledge base status label
   */
  const getKnowledgeBaseStatus = () => {
    if (reindexing) {
      return { label: 'Syncing...', color: 'text-orange-600', bg: 'bg-orange-50' };
    }
    
    if (reindexStatus.status === 'completed') {
      return { label: 'Synced', color: 'text-green-600', bg: 'bg-green-50' };
    }
    
    if (reindexStatus.status === 'failed') {
      return { label: 'Outdated (Failed)', color: 'text-red-600', bg: 'bg-red-50' };
    }
    
    return { label: 'Unknown', color: 'text-gray-600', bg: 'bg-gray-50' };
  };

  const kbStatus = getKnowledgeBaseStatus();

  return (
    <Layout
      title="Admin - System Status"
      description="Monitor system health and performance"
    >
      <AdminGuard>
        <div className="container margin-vert--lg">
          {/* Navigation Tabs */}
          <div className="margin-bottom--lg">
            <div className="row">
              <div className="col col--6">
                <a
                  href="/physical-ai-humanoid-robotics-textbook/admin/ingest"
                  className="button button--secondary button--lg margin-right--md"
                >
                  📤 Knowledge Base
                </a>
                <a
                  href="/physical-ai-humanoid-robotics-textbook/admin/status"
                  className="button button--primary button--lg"
                >
                  🛡️ System Status
                </a>
              </div>
            </div>
          </div>

          {/* Header */}
          <div className="margin-bottom--xl">
            <h1 className="text-3xl font-bold" style={{ color: '#ff6b35' }}>
              🛡️ System Status Dashboard
            </h1>
            <p className="text-lg text-gray-600 margin-top--sm">
              Monitor system health, performance metrics, and knowledge base status
            </p>
            {user && (
              <p className="text-sm text-gray-500 margin-top--sm">
                Logged in as: <span className="font-medium">{user.email}</span>
              </p>
            )}
          </div>

          {/* Error Alert */}
          {error && (
            <div className="alert alert--danger margin-bottom--lg">
              <p className="margin--none">{error}</p>
            </div>
          )}

          {/* Knowledge Base Status */}
          <section className="margin-bottom--lg">
            <div
              className={`card ${kbStatus.bg} border-2 border-gray-300 shadow--md`}
            >
              <div className="card__header">
                <h2 className="text-xl font-bold margin--none">
                  📚 Knowledge Base Status
                </h2>
              </div>
              <div className="card__body">
                <div className="flex justify-between items-center">
                  <div>
                    <p className="text-lg margin--none">
                      Status: <span className={`font-bold ${kbStatus.color}`}>{kbStatus.label}</span>
                    </p>
                    {reindexStatus.progress && (
                      <p className="text-sm text-gray-600 margin-top--sm">
                        {reindexStatus.progress.processed_files} / {reindexStatus.progress.total_files} files processed
                      </p>
                    )}
                  </div>
                  
                  <button
                    className="button button--primary"
                    onClick={handleTriggerReindex}
                    disabled={reindexing}
                  >
                    {reindexing ? '⏳ Syncing...' : '🔄 Sync Knowledge Base'}
                  </button>
                </div>

                {/* Progress Bar */}
                {reindexing && reindexStatus.progress && (
                  <div className="margin-top--md">
                    <div className="progress-bar">
                      <div
                        className="progress-bar progress-bar--success"
                        role="progressbar"
                        style={{ width: `${reindexStatus.progress.percent_complete}%` }}
                        aria-valuenow={reindexStatus.progress.percent_complete}
                        aria-valuemin={0}
                        aria-valuemax={100}
                      />
                    </div>
                    <p className="text-xs text-gray-500 margin-top--sm">
                      {reindexStatus.progress.percent_complete}% complete
                      {reindexStatus.current_file && (
                        <span> - Processing: {reindexStatus.current_file}</span>
                      )}
                    </p>
                  </div>
                )}

                {/* Last Synced */}
                {reindexStatus.timing?.completed_at && (
                  <p className="text-sm text-gray-500 margin-top--md">
                    Last synced: {new Date(reindexStatus.timing.completed_at).toLocaleString()}
                  </p>
                )}
              </div>
            </div>
          </section>

          {/* System Health */}
          {loading ? (
            <p>Loading health data...</p>
          ) : healthData ? (
            <section className="margin-bottom--lg">
              <h2 className="text-2xl font-bold margin-bottom--md" style={{ color: '#06b6d4' }}>
                🔍 System Health
              </h2>
              <div className="row">
                <div className="col col--4">
                  <HealthCard
                    serviceName="PostgreSQL"
                    status={healthData.services.postgresql.status}
                    responseTimeMs={healthData.services.postgresql.response_time_ms}
                    error={healthData.services.postgresql.error}
                    lastChecked={healthData.services.postgresql.last_checked}
                  />
                </div>
                <div className="col col--4">
                  <HealthCard
                    serviceName="Qdrant"
                    status={healthData.services.qdrant.status}
                    responseTimeMs={healthData.services.qdrant.response_time_ms}
                    error={healthData.services.qdrant.error}
                    lastChecked={healthData.services.qdrant.last_checked}
                    collection={healthData.services.qdrant.collection}
                    documentCount={healthData.services.qdrant.document_count}
                  />
                </div>
                <div className="col col--4">
                  <HealthCard
                    serviceName="Grok API"
                    status={healthData.services.grok_api.status}
                    responseTimeMs={healthData.services.grok_api.response_time_ms}
                    error={healthData.services.grok_api.error}
                    lastChecked={healthData.services.grok_api.last_checked}
                    endpoint={healthData.services.grok_api.endpoint}
                  />
                </div>
              </div>
              
              {/* Overall Status */}
              <div className={`alert margin-top--md ${
                healthData.overall_status === 'healthy' ? 'alert--success' :
                healthData.overall_status === 'degraded' ? 'alert--warning' : 'alert--danger'
              }`}>
                <p className="margin--none">
                  <strong>Overall Status:</strong> {healthData.overall_status.toUpperCase()}
                </p>
              </div>
            </section>
          ) : (
            <p>Failed to load health data</p>
          )}

          {/* Performance Metrics */}
          {loading ? (
            <p>Loading stats...</p>
          ) : statsData ? (
            <section>
              <h2 className="text-2xl font-bold margin-bottom--md" style={{ color: '#ff6b35' }}>
                📊 Performance Metrics
              </h2>
              <div className="row">
                {/* RAG Latency */}
                <div className="col col--6">
                  <div className="card shadow--md">
                    <div className="card__header">
                      <h3 className="text-lg font-bold margin--none">RAG Latency</h3>
                    </div>
                    <div className="card__body">
                      <div className="margin-bottom--sm">
                        <strong>Avg:</strong> <span className="text-green-600">{statsData.rag_latency.avg_ms}ms</span>
                      </div>
                      <div className="margin-bottom--sm">
                        <strong>P95:</strong> <span className="text-yellow-600">{statsData.rag_latency.p95_ms}ms</span>
                      </div>
                      <div className="margin-bottom--sm">
                        <strong>P99:</strong> <span className="text-orange-600">{statsData.rag_latency.p99_ms}ms</span>
                      </div>
                      <div className="text-xs text-gray-500">
                        Samples: {statsData.rag_latency.sample_count}
                      </div>
                    </div>
                  </div>
                </div>

                {/* LLM Latency */}
                <div className="col col--6">
                  <div className="card shadow--md">
                    <div className="card__header">
                      <h3 className="text-lg font-bold margin--none">LLM Latency (Grok)</h3>
                    </div>
                    <div className="card__body">
                      <div className="margin-bottom--sm">
                        <strong>Avg:</strong> <span className="text-green-600">{statsData.llm_latency.avg_ms}ms</span>
                      </div>
                      <div className="margin-bottom--sm">
                        <strong>P95:</strong> <span className="text-yellow-600">{statsData.llm_latency.p95_ms}ms</span>
                      </div>
                      <div className="margin-bottom--sm">
                        <strong>P99:</strong> <span className="text-orange-600">{statsData.llm_latency.p99_ms}ms</span>
                      </div>
                      <div className="text-xs text-gray-500">
                        Samples: {statsData.llm_latency.sample_count}
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Usage Analytics */}
              <div className="card shadow--md margin-top--md">
                <div className="card__header">
                  <h3 className="text-lg font-bold margin--none">Usage Analytics</h3>
                </div>
                <div className="card__body">
                  <div className="row">
                    <div className="col col--4">
                      <div className="text-3xl font-bold text-blue-600">
                        {statsData.usage_analytics.total_queries}
                      </div>
                      <div className="text-sm text-gray-600">Total Queries</div>
                    </div>
                    <div className="col col--4">
                      <div className="text-3xl font-bold text-purple-600">
                        {statsData.usage_analytics.total_tokens.toLocaleString()}
                      </div>
                      <div className="text-sm text-gray-600">Total Tokens</div>
                    </div>
                    <div className="col col--4">
                      <div className="text-3xl font-bold text-green-600">
                        {statsData.usage_analytics.unique_users}
                      </div>
                      <div className="text-sm text-gray-600">Unique Users</div>
                    </div>
                  </div>
                </div>
              </div>
            </section>
          ) : (
            <p>Failed to load stats data</p>
          )}
        </div>
      </AdminGuard>
    </Layout>
  );
}
