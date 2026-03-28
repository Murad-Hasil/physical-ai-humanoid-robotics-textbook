/**
 * Translation Toggle for Phase 7 - Final Intelligence.
 * 
 * Allows users to toggle between English and Roman Urdu translations.
 */

import React from 'react';

interface TranslationToggleProps {
  currentLang: 'en' | 'ur-Latn';
  onToggle: (newLang: 'en' | 'ur-Latn') => void;
  translationAvailable?: boolean;
  isLoading?: boolean;
}

export const TranslationToggle: React.FC<TranslationToggleProps> = ({
  currentLang,
  onToggle,
  translationAvailable = true,
  isLoading = false,
}) => {
  const handleToggle = () => {
    if (!translationAvailable || isLoading) return;
    onToggle(currentLang === 'en' ? 'ur-Latn' : 'en');
  };

  return (
    <div className="translation-toggle flex items-center gap-2">
      <span className="text-sm text-gray-400">Language:</span>
      
      <button
        onClick={handleToggle}
        disabled={!translationAvailable || isLoading}
        className={`relative px-4 py-2 rounded border-2 transition-all font-semibold ${
          currentLang === 'en'
            ? 'border-[#00F3FF] text-[#00F3FF] neon-border'
            : 'border-gray-600 text-gray-400 hover:border-[#00F3FF]'
        } ${!translationAvailable ? 'opacity-50 cursor-not-allowed' : ''} ${
          isLoading ? 'animate-pulse' : ''
        }`}
        title={translationAvailable ? 'Toggle language' : 'Translation not available'}
      >
        {isLoading ? (
          <span className="flex items-center gap-2">
            <span className="w-2 h-2 bg-[#00F3FF] rounded-full animate-ping"></span>
            Loading...
          </span>
        ) : (
          <span className="flex items-center gap-2">
            <span>{currentLang === 'en' ? '🇬🇧' : '📝'}</span>
            {currentLang === 'en' ? 'EN' : 'اردو'}
          </span>
        )}
      </button>

      {!translationAvailable && currentLang === 'ur-Latn' && (
        <span className="text-xs text-[#A0A0B0]">
          Not available for this chapter
        </span>
      )}
    </div>
  );
};

export default TranslationToggle;
