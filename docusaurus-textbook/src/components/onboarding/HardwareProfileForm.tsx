/**
 * Hardware Profile Form for Phase 7 - Final Intelligence.
 * 
 * Allows users to select and configure their hardware setup:
 * - Sim Rig (RTX 4070 Ti+)
 * - Edge Kit (Jetson Orin)
 * - Unitree Robots
 */

import React, { useState, useEffect } from 'react';

type HardwareType = 'sim_rig' | 'edge_kit' | 'unitree';

interface HardwareProfileData {
  hardware_type: HardwareType;
  gpu_model?: string;
  gpu_vram_gb?: number;
  ubuntu_version?: string;
  edge_kit_type?: string;
  jetpack_version?: string;
  robot_model?: string;
}

interface HardwareProfileFormProps {
  onSubmit: (data: HardwareProfileData) => Promise<void>;
  initialValues?: Partial<HardwareProfileData>;
  isLoading?: boolean;
}

export const HardwareProfileForm: React.FC<HardwareProfileFormProps> = ({
  onSubmit,
  initialValues,
  isLoading = false,
}) => {
  const [hardwareType, setHardwareType] = useState<HardwareType>(
    initialValues?.hardware_type || 'sim_rig'
  );
  const [gpuModel, setGpuModel] = useState(initialValues?.gpu_model || '');
  const [gpuVram, setGpuVram] = useState(initialValues?.gpu_vram_gb?.toString() || '');
  const [ubuntuVersion, setUbuntuVersion] = useState(initialValues?.ubuntu_version || '');
  const [edgeKitType, setEdgeKitType] = useState(initialValues?.edge_kit_type || '');
  const [jetpackVersion, setJetpackVersion] = useState(initialValues?.jetpack_version || '');
  const [robotModel, setRobotModel] = useState(initialValues?.robot_model || '');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);

    try {
      const data: HardwareProfileData = {
        hardware_type: hardwareType,
        ...(hardwareType === 'sim_rig' && {
          gpu_model: gpuModel || undefined,
          gpu_vram_gb: gpuVram ? parseInt(gpuVram, 10) : undefined,
          ubuntu_version: ubuntuVersion || undefined,
        }),
        ...(hardwareType === 'edge_kit' && {
          edge_kit_type: edgeKitType || undefined,
          jetpack_version: jetpackVersion || undefined,
          ubuntu_version: ubuntuVersion || undefined,
        }),
        ...(hardwareType === 'unitree' && {
          robot_model: robotModel || undefined,
        }),
      };

      await onSubmit(data);
    } catch (error) {
      console.error('Failed to submit hardware profile:', error);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="glass-panel p-6 rounded-lg cyber-form">
      <h3 className="text-xl font-bold mb-4 text-[#00F3FF]">Hardware Configuration</h3>

      {/* Hardware Type Selection */}
      <div className="mb-6">
        <label className="block text-sm font-medium mb-2">Hardware Type</label>
        <div className="grid grid-cols-3 gap-4">
          <button
            type="button"
            onClick={() => setHardwareType('sim_rig')}
            className={`p-4 rounded border-2 transition-all ${
              hardwareType === 'sim_rig'
                ? 'border-[#00F3FF] neon-border bg-cyan-900/20'
                : 'border-gray-600 hover:border-[#00F3FF]'
            }`}
          >
            <div className="text-2xl mb-2">🖥️</div>
            <div className="font-semibold">Sim Rig</div>
            <div className="text-xs text-gray-400">RTX 4070 Ti+</div>
          </button>

          <button
            type="button"
            onClick={() => setHardwareType('edge_kit')}
            className={`p-4 rounded border-2 transition-all ${
              hardwareType === 'edge_kit'
                ? 'border-[#00F3FF] neon-border bg-cyan-900/20'
                : 'border-gray-600 hover:border-[#00F3FF]'
            }`}
          >
            <div className="text-2xl mb-2">🔧</div>
            <div className="font-semibold">Edge Kit</div>
            <div className="text-xs text-gray-400">Jetson Orin</div>
          </button>

          <button
            type="button"
            onClick={() => setHardwareType('unitree')}
            className={`p-4 rounded border-2 transition-all ${
              hardwareType === 'unitree'
                ? 'border-[#00F3FF] neon-border bg-cyan-900/20'
                : 'border-gray-600 hover:border-[#00F3FF]'
            }`}
          >
            <div className="text-2xl mb-2">🤖</div>
            <div className="font-semibold">Unitree</div>
            <div className="text-xs text-gray-400">Go2 / G1</div>
          </button>
        </div>
      </div>

      {/* Sim Rig Fields */}
      {hardwareType === 'sim_rig' && (
        <>
          <div className="mb-4">
            <label className="block text-sm font-medium mb-2">GPU Model</label>
            <input
              type="text"
              value={gpuModel}
              onChange={(e) => setGpuModel(e.target.value)}
              placeholder="e.g., RTX 4070 Ti, RTX 4090"
              className="w-full px-4 py-2 bg-black/50 border border-[#00F3FF] rounded text-white focus:outline-none focus:neon-border"
            />
          </div>

          <div className="mb-4">
            <label className="block text-sm font-medium mb-2">GPU VRAM (GB)</label>
            <input
              type="number"
              value={gpuVram}
              onChange={(e) => setGpuVram(e.target.value)}
              placeholder="e.g., 12, 16, 24"
              min="1"
              max="128"
              className="w-full px-4 py-2 bg-black/50 border border-[#00F3FF] rounded text-white focus:outline-none focus:neon-border"
            />
          </div>

          <div className="mb-4">
            <label className="block text-sm font-medium mb-2">Ubuntu Version</label>
            <input
              type="text"
              value={ubuntuVersion}
              onChange={(e) => setUbuntuVersion(e.target.value)}
              placeholder="e.g., 22.04, 24.04"
              className="w-full px-4 py-2 bg-black/50 border border-[#00F3FF] rounded text-white focus:outline-none focus:neon-border"
            />
          </div>
        </>
      )}

      {/* Edge Kit Fields */}
      {hardwareType === 'edge_kit' && (
        <>
          <div className="mb-4">
            <label className="block text-sm font-medium mb-2">Edge Device</label>
            <select
              value={edgeKitType}
              onChange={(e) => setEdgeKitType(e.target.value)}
              className="w-full px-4 py-2 bg-black/50 border border-[#00F3FF] rounded text-white focus:outline-none focus:neon-border"
            >
              <option value="">Select device...</option>
              <option value="Jetson Orin Nano">Jetson Orin Nano</option>
              <option value="Jetson Orin NX">Jetson Orin NX</option>
              <option value="Jetson AGX Orin">Jetson AGX Orin</option>
            </select>
          </div>

          <div className="mb-4">
            <label className="block text-sm font-medium mb-2">JetPack Version</label>
            <input
              type="text"
              value={jetpackVersion}
              onChange={(e) => setJetpackVersion(e.target.value)}
              placeholder="e.g., 5.1, 6.0"
              className="w-full px-4 py-2 bg-black/50 border border-[#00F3FF] rounded text-white focus:outline-none focus:neon-border"
            />
          </div>

          <div className="mb-4">
            <label className="block text-sm font-medium mb-2">Ubuntu Version</label>
            <input
              type="text"
              value={ubuntuVersion}
              onChange={(e) => setUbuntuVersion(e.target.value)}
              placeholder="e.g., 22.04"
              className="w-full px-4 py-2 bg-black/50 border border-[#00F3FF] rounded text-white focus:outline-none focus:neon-border"
            />
          </div>
        </>
      )}

      {/* Unitree Fields */}
      {hardwareType === 'unitree' && (
        <>
          <div className="mb-4">
            <label className="block text-sm font-medium mb-2">Robot Model</label>
            <select
              value={robotModel}
              onChange={(e) => setRobotModel(e.target.value)}
              className="w-full px-4 py-2 bg-black/50 border border-[#00F3FF] rounded text-white focus:outline-none focus:neon-border"
            >
              <option value="">Select robot...</option>
              <option value="Unitree Go2">Unitree Go2</option>
              <option value="Unitree G1">Unitree G1</option>
              <option value="Proxy">Proxy</option>
            </select>
          </div>
        </>
      )}

      {/* Submit Button */}
      <button
        type="submit"
        disabled={isSubmitting || isLoading}
        className="w-full py-3 px-6 cyber-button font-bold disabled:opacity-50 disabled:cursor-not-allowed"
      >
        {isSubmitting ? 'Saving...' : isLoading ? 'Loading...' : 'Save Hardware Profile'}
      </button>
    </form>
  );
};

export default HardwareProfileForm;
