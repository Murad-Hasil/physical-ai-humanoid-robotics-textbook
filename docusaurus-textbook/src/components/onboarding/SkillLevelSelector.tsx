/**
 * Skill Level Selector for Phase 7 - Final Intelligence.
 * 
 * Allows users to select their skill level:
 * - Beginner: Foundational concepts, simple language
 * - Intermediate: Technical details, assumes basic knowledge
 * - Advanced: Deep optimization, production considerations
 */

import React from 'react';

type SkillLevel = 'beginner' | 'intermediate' | 'advanced';

interface SkillLevelSelectorProps {
  value: SkillLevel;
  onChange: (level: SkillLevel) => void;
  disabled?: boolean;
  showDescriptions?: boolean;
  direction?: 'vertical' | 'horizontal';
}

const skillLevels: { value: SkillLevel; label: string; description: string; icon: string }[] = [
  {
    value: 'beginner',
    label: 'Beginner',
    description: 'New to Physical AI. I want foundational concepts and step-by-step guidance.',
    icon: '🌱',
  },
  {
    value: 'intermediate',
    label: 'Intermediate',
    description: 'Some experience with AI/robotics. I understand basic concepts and want technical details.',
    icon: '🚀',
  },
  {
    value: 'advanced',
    label: 'Advanced',
    description: 'Experienced practitioner. I want optimization strategies and production considerations.',
    icon: '⚡',
  },
];

export const SkillLevelSelector: React.FC<SkillLevelSelectorProps> = ({
  value,
  onChange,
  disabled = false,
  showDescriptions = true,
  direction = 'vertical',
}) => {
  const handleSelect = (level: SkillLevel) => {
    if (!disabled) {
      onChange(level);
    }
  };

  return (
    <div className={`space-y-4 ${direction === 'horizontal' ? 'grid grid-cols-3 gap-4' : ''}`}>
      {skillLevels.map((level) => (
        <button
          key={level.value}
          type="button"
          onClick={() => handleSelect(level.value)}
          disabled={disabled}
          className={`w-full p-4 rounded-lg border-2 transition-all text-left ${
            value === level.value
              ? 'border-[#00F3FF] neon-border bg-cyan-900/20'
              : 'border-gray-600 hover:border-[#00F3FF]'
          } ${disabled ? 'opacity-50 cursor-not-allowed' : ''}`}
        >
          <div className="flex items-center mb-2">
            <span className="text-2xl mr-2">{level.icon}</span>
            <span className="font-bold text-[#00F3FF]">{level.label}</span>
          </div>
          
          {showDescriptions && (
            <p className="text-sm text-gray-300 leading-relaxed">
              {level.description}
            </p>
          )}
        </button>
      ))}
    </div>
  );
};

export default SkillLevelSelector;
