/**
 * Hardware Indicator for Phase 7 - Final Intelligence.
 * 
 * Displays current user's hardware profile and skill level.
 */

import React from 'react';
import { usePersonalization } from '../../context/PersonalizationContext';

interface HardwareIndicatorProps {
  compact?: boolean;
  onEdit?: () => void;
}

const hardwareIcons: Record<string, string> = {
  sim_rig: '🖥️',
  edge_kit: '🔧',
  unitree: '🤖',
};

const hardwareLabels: Record<string, string> = {
  sim_rig: 'Sim Rig',
  edge_kit: 'Edge Kit',
  unitree: 'Unitree',
};

const skillLevelColors: Record<string, string> = {
  beginner: 'bg-green-500',
  intermediate: 'bg-yellow-500',
  advanced: 'bg-red-500',
};

export const HardwareIndicator: React.FC<HardwareIndicatorProps> = ({
  compact = false,
  onEdit,
}) => {
  const { hardwareProfile, skillLevel } = usePersonalization();

  if (!hardwareProfile) {
    return null;
  }

  const hardwareType = hardwareProfile.hardware_type;
  const icon = hardwareIcons[hardwareType] || '❓';
  const label = hardwareLabels[hardwareType] || hardwareType;

  if (compact) {
    return (
      <div className="hardware-indicator-compact flex items-center gap-2 text-sm">
        <span className="text-lg">{icon}</span>
        <span className="font-semibold text-[#00F3FF]">{label}</span>
        <span
          className={`px-2 py-0.5 rounded text-xs font-medium text-white ${
            skillLevelColors[skillLevel]
          }`}
        >
          {skillLevel}
        </span>
        {onEdit && (
          <button
            onClick={onEdit}
            className="text-xs text-gray-400 hover:text-[#00F3FF] underline"
          >
            Edit
          </button>
        )}
      </div>
    );
  }

  return (
    <div className="glass-panel p-4 rounded-lg border border-[#00F3FF]/30">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <span className="text-3xl">{icon}</span>
          <div>
            <div className="font-bold text-[#00F3FF]">{label}</div>
            <div className="text-sm text-gray-400">
              {hardwareProfile.gpu_model && (
                <span>{hardwareProfile.gpu_model} • </span>
              )}
              {hardwareProfile.edge_kit_type && (
                <span>{hardwareProfile.edge_kit_type} • </span>
              )}
              {hardwareProfile.robot_model && (
                <span>{hardwareProfile.robot_model} • </span>
              )}
              <span className="capitalize">{skillLevel}</span>
            </div>
          </div>
        </div>
        {onEdit && (
          <button
            onClick={onEdit}
            className="px-4 py-2 cyber-button text-sm font-semibold"
          >
            Edit Profile
          </button>
        )}
      </div>
    </div>
  );
};

export default HardwareIndicator;
