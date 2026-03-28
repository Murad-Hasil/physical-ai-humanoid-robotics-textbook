/**
 * Personalization Toggle for Phase 7 - Final Intelligence.
 * 
 * Allows users to enable/disable AI-powered personalization.
 */

import React from 'react';

interface PersonalizationToggleProps {
  enabled: boolean;
  onToggle: (enabled: boolean) => void;
  size?: 'sm' | 'md' | 'lg';
}

export const PersonalizationToggle: React.FC<PersonalizationToggleProps> = ({
  enabled,
  onToggle,
  size = 'md',
}) => {
  const sizeClasses = {
    sm: 'w-10 h-5',
    md: 'w-12 h-6',
    lg: 'w-14 h-7',
  };

  const knobSizeClasses = {
    sm: 'w-4 h-4',
    md: 'w-5 h-5',
    lg: 'w-6 h-6',
  };

  return (
    <button
      onClick={() => onToggle(!enabled)}
      className={`${sizeClasses[size]} rounded-full transition-colors relative ${
        enabled ? 'bg-[#00F3FF]' : 'bg-gray-600'
      }`}
      title={enabled ? 'Disable personalization' : 'Enable personalization'}
    >
      <span
        className={`absolute top-0.5 left-0.5 ${knobSizeClasses[size]} bg-white rounded-full transition-transform ${
          enabled ? 'translate-x-full -ml-5' : ''
        }`}
      />
    </button>
  );
};

export default PersonalizationToggle;
