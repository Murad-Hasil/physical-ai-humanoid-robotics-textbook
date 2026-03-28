/**
 * Custom DocItem wrapper with personalization and translation controls.
 *
 * Wraps the default DocItem component to add:
 * - Translation toggle (English ↔ Roman Urdu)
 * - Personalization toggle
 * - Hardware profile indicator
 * - Personalized summary display
 */

import React, { useState, useEffect } from 'react';
import OriginalDocItem from '@theme-original/DocItem';
import { usePersonalization } from '@site/src/context/PersonalizationContext';
import TranslationToggle from '@site/src/components/translation/TranslationToggle';
import TranslationProgress from '@site/src/components/translation/TranslationProgress';
import HardwareIndicator from '@site/src/components/personalization/HardwareIndicator';
import PersonalizationToggle from '@site/src/components/personalization/PersonalizationToggle';
import axios from 'axios';

const API_BASE_URL = 'https://mb-murad-physical-ai-backend.hf.space/api/v1';

export default function DocItem(props: any) {
  const {
    language,
    setLanguage,
    personalizationEnabled,
    setPersonalizationEnabled,
    hardwareProfile,
    skillLevel,
  } = usePersonalization();

  const [personalizedSummary, setPersonalizedSummary] = useState<string | null>(null);
  const [translationContent, setTranslationContent] = useState<string | null>(null);
  const [translationAvailable, setTranslationAvailable] = useState(false);
  const [isLoadingSummary, setIsLoadingSummary] = useState(false);
  const [isLoadingTranslation, setIsLoadingTranslation] = useState(false);

  const chapterId = props.content?.metadata?.id;

  // Fetch personalized summary when personalization is enabled
  useEffect(() => {
    const fetchPersonalizedSummary = async () => {
      if (!personalizationEnabled || !chapterId || !hardwareProfile) {
        setPersonalizedSummary(null);
        return;
      }

      setIsLoadingSummary(true);
      try {
        const token = localStorage.getItem('access_token');
        const params = new URLSearchParams();
        if (hardwareProfile.hardware_type) {
          params.append('hardware_profile', hardwareProfile.hardware_type);
        }
        if (skillLevel) {
          params.append('skill_level', skillLevel);
        }

        const response = await axios.get(
          `${API_BASE_URL}/chapters/${chapterId}/summary?${params}`,
          {
            headers: token ? { Authorization: `Bearer ${token}` } : {},
          }
        );

        setPersonalizedSummary(response.data.summary_content);
      } catch (error) {
        console.error('Failed to fetch personalized summary:', error);
        setPersonalizedSummary(null);
      } finally {
        setIsLoadingSummary(false);
      }
    };

    fetchPersonalizedSummary();
  }, [personalizationEnabled, chapterId, hardwareProfile, skillLevel]);

  // Fetch translation when language is set to Roman Urdu
  useEffect(() => {
    const fetchTranslation = async () => {
      if (language !== 'ur-Latn' || !chapterId) {
        setTranslationContent(null);
        setTranslationAvailable(false);
        return;
      }

      setIsLoadingTranslation(true);
      try {
        const token = localStorage.getItem('access_token');
        const response = await axios.get(
          `${API_BASE_URL}/chapters/${chapterId}/translation?lang=ur-Latn`,
          {
            headers: token ? { Authorization: `Bearer ${token}` } : {},
          }
        );

        setTranslationContent(response.data.translated_content);
        setTranslationAvailable(response.data.status === 'published');
      } catch (error) {
        console.error('Failed to fetch translation:', error);
        setTranslationContent(null);
        setTranslationAvailable(false);
      } finally {
        setIsLoadingTranslation(false);
      }
    };

    fetchTranslation();
  }, [language, chapterId]);

  // Determine content to display
  const displayContent = translationContent || props.content;

  return (
    <>
      {/* Personalization & translation controls bar — above the doc */}
      <div className="mb-6 space-y-4" style={{ padding: '0 var(--ifm-spacing-horizontal)' }}>
        {/* Top bar */}
        <div className="flex items-center justify-between">
          <TranslationToggle
            currentLang={language}
            onToggle={setLanguage}
            translationAvailable={translationAvailable}
            isLoading={isLoadingTranslation}
          />

          <div className="flex items-center gap-4">
            <span className="text-sm text-gray-400">AI Personalization:</span>
            <PersonalizationToggle
              enabled={personalizationEnabled}
              onToggle={setPersonalizationEnabled}
            />
          </div>
        </div>

        {/* Hardware profile indicator */}
        {personalizationEnabled && hardwareProfile && (
          <HardwareIndicator compact onEdit={() => { window.location.href = '/profile'; }} />
        )}

        {/* Personalized summary */}
        {personalizationEnabled && personalizedSummary && (
          <div className="glass-panel p-4 rounded-lg border border-[#00F3FF]/30">
            <h3 className="text-lg font-bold text-[#00F3FF] mb-2">
              ✨ Personalized Summary
            </h3>
            <div
              className="prose prose-invert max-w-none"
              dangerouslySetInnerHTML={{ __html: personalizedSummary }}
            />
          </div>
        )}

        {/* Translation in progress indicator */}
        {language === 'ur-Latn' && !translationAvailable && !isLoadingTranslation && (
          <TranslationProgress status="draft" />
        )}
      </div>

      {/* Original DocItem renders the actual doc content */}
      <OriginalDocItem {...props} content={displayContent} />
    </>
  );
}
