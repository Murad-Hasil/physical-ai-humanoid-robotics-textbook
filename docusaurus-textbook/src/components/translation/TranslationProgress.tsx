/**
 * Translation Progress Indicator for Phase 7 - Final Intelligence.
 * 
 * Shows the status of AI translation (draft, in_review, published).
 */

import React from 'react';

type TranslationStatus = 'draft' | 'in_review' | 'published';

interface TranslationProgressProps {
  status: TranslationStatus;
  compact?: boolean;
}

const statusConfig: Record<TranslationStatus, { color: string; icon: string; label: string }> = {
  draft: {
    color: 'text-[#FFD700]',
    icon: '🔄',
    label: 'AI Translation in progress',
  },
  in_review: {
    color: 'text-[#FF6B35]',
    icon: '👁️',
    label: 'Under review',
  },
  published: {
    color: 'text-[#00FF00]',
    icon: '✅',
    label: 'Published',
  },
};

export const TranslationProgress: React.FC<TranslationProgressProps> = ({
  status,
  compact = false,
}) => {
  const config = statusConfig[status];

  if (compact) {
    return (
      <span className={`text-lg ${config.color}`} title={config.label}>
        {config.icon}
      </span>
    );
  }

  return (
    <div className={`flex items-center gap-2 text-sm ${config.color}`}>
      <span className="text-lg">{config.icon}</span>
      <span className="font-medium">{config.label}</span>
    </div>
  );
};

export default TranslationProgress;
