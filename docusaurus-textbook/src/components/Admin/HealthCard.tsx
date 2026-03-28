/**
 * Health Card Component
 *
 * Displays health status for a single service with neon color coding.
 */

import React from 'react';

interface HealthCardProps {
  serviceName: string;
  status: 'healthy' | 'unhealthy' | 'degraded';
  responseTimeMs?: number;
  error?: string;
  lastChecked?: string;
  // Additional fields for specific services
  collection?: string;
  documentCount?: number;
  endpoint?: string;
}

export default function HealthCard({
  serviceName,
  status,
  responseTimeMs,
  error,
  lastChecked,
  collection,
  documentCount,
  endpoint,
}: HealthCardProps) {
  // Determine color scheme based on status
  const getStatusColors = () => {
    switch (status) {
      case 'healthy':
        return {
          bg: 'bg-green-50',
          border: 'border-green-500',
          text: 'text-green-700',
          badge: 'bg-green-500',
          badgeText: 'text-white',
          icon: '✓',
          label: 'Online',
        };
      case 'degraded':
        return {
          bg: 'bg-orange-50',
          border: 'border-orange-500',
          text: 'text-orange-700',
          badge: 'bg-orange-500',
          badgeText: 'text-white',
          icon: '⚠',
          label: 'Degraded',
        };
      case 'unhealthy':
      default:
        return {
          bg: 'bg-red-50',
          border: 'border-red-500',
          text: 'text-red-700',
          badge: 'bg-red-500',
          badgeText: 'text-white',
          icon: '✗',
          label: 'Offline',
        };
    }
  };

  const colors = getStatusColors();

  // Format last checked time
  const formatLastChecked = (timestamp?: string) => {
    if (!timestamp) return 'Never';
    try {
      const date = new Date(timestamp);
      return date.toLocaleString();
    } catch {
      return timestamp;
    }
  };

  return (
    <div
      className={`card ${colors.bg} ${colors.border} border-2 shadow--md`}
    >
      <div className="card__header">
        <div className="flex justify-between items-center">
          <h3 className="text-lg font-bold margin--none">{serviceName}</h3>
          <span
            className={`badge ${colors.badge} ${colors.badgeText} padding-horiz--md padding-vert--sm`}
          >
            {colors.icon} {colors.label}
          </span>
        </div>
      </div>

      <div className="card__body">
        {/* Response Time */}
        {responseTimeMs !== undefined && (
          <div className="margin-bottom--sm">
            <strong>Response Time:</strong>{' '}
            <span className={colors.text}>{responseTimeMs}ms</span>
          </div>
        )}

        {/* Collection Info (for Qdrant) */}
        {collection && (
          <div className="margin-bottom--sm">
            <strong>Collection:</strong> <code>{collection}</code>
          </div>
        )}

        {/* Document Count (for Qdrant) */}
        {documentCount !== undefined && (
          <div className="margin-bottom--sm">
            <strong>Documents:</strong> {documentCount.toLocaleString()}
          </div>
        )}

        {/* Endpoint (for Grok API) */}
        {endpoint && (
          <div className="margin-bottom--sm">
            <strong>Endpoint:</strong> <code className="text-xs">{endpoint}</code>
          </div>
        )}

        {/* Error Message */}
        {error && (
          <div className={`alert alert--danger margin-top--md`}>
            <p className="margin--none text-sm">{error}</p>
          </div>
        )}

        {/* Last Checked */}
        <div className="margin-top--md text-xs text-gray-500">
          Last checked: {formatLastChecked(lastChecked)}
        </div>
      </div>
    </div>
  );
}
