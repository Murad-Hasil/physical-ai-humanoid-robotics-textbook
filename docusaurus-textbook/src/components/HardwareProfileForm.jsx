/**
 * Hardware Profile Form Component
 * 
 * Form for selecting and saving hardware configuration per PDF Page 5.
 */

import React, { useState, useEffect } from 'react';
import { useHardware } from '@site/src/context/HardwareContext';
import clsx from 'clsx';

// Hardware options from PDF Page 5
const WORKSTATION_OPTIONS = [
  { value: 'RTX 4070 Ti', label: 'NVIDIA RTX 4070 Ti (12GB)' },
  { value: 'RTX 4080', label: 'NVIDIA RTX 4080 (16GB)' },
  { value: 'RTX 4090', label: 'NVIDIA RTX 4090 (24GB)' },
  { value: 'Custom', label: 'Custom Configuration' },
];

const EDGE_KIT_OPTIONS = [
  { value: 'Jetson Orin Nano', label: 'Jetson Orin Nano' },
  { value: 'Jetson Orin NX', label: 'Jetson Orin NX' },
];

const ROBOT_OPTIONS = [
  { value: 'Unitree Go2', label: 'Unitree Go2 (Quadruped)' },
  { value: 'Unitree G1', label: 'Unitree G1 (Humanoid)' },
  { value: 'Simulation Proxy', label: 'Simulation Proxy (Virtual)' },
];

export default function HardwareProfileForm() {
  const { hardwareProfile, loading, error, updateHardwareProfile } = useHardware();
  const [formData, setFormData] = useState({
    hardware_type: 'sim_rig',
    gpu_model: '',
    gpu_vram_gb: 12,
    edge_kit_type: '',
    robot_model: '',
  });
  const [saving, setSaving] = useState(false);
  const [saveStatus, setSaveStatus] = useState(null);

  // Populate form with existing data
  useEffect(() => {
    if (hardwareProfile) {
      setFormData({
        hardware_type: hardwareProfile.hardware_type || 'sim_rig',
        gpu_model: hardwareProfile.gpu_model || '',
        gpu_vram_gb: hardwareProfile.gpu_vram_gb || 12,
        edge_kit_type: hardwareProfile.edge_kit_type || '',
        robot_model: hardwareProfile.robot_model || '',
      });
    }
  }, [hardwareProfile]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSaving(true);
    setSaveStatus(null);

    // Prepare data based on hardware type
    const payload = {
      hardware_type: formData.hardware_type,
    };

    if (formData.hardware_type === 'sim_rig') {
      payload.gpu_model = formData.gpu_model;
      payload.gpu_vram_gb = formData.gpu_vram_gb;
    } else if (formData.hardware_type === 'edge_kit') {
      payload.edge_kit_type = formData.edge_kit_type;
    }

    if (formData.robot_model) {
      payload.robot_model = formData.robot_model;
    }

    const result = await updateHardwareProfile(payload);

    if (result.success) {
      setSaveStatus({ type: 'success', message: 'Hardware profile saved successfully!' });
    } else {
      setSaveStatus({ type: 'error', message: result.error || 'Failed to save profile' });
    }

    setSaving(false);
  };

  if (loading) {
    return (
      <div className="text--center padding--lg">
        <div className="spinner"></div>
        <p>Loading your hardware profile...</p>
      </div>
    );
  }

  return (
    <form onSubmit={handleSubmit} className="hardware-form">
      {/* Hardware Type Selection */}
      <div className="form-group margin-bottom--lg">
        <label className="form-label" htmlFor="hardware_type">
          Hardware Type
        </label>
        <select
          id="hardware_type"
          name="hardware_type"
          value={formData.hardware_type}
          onChange={handleChange}
          className="form-select glass-input"
          required
        >
          <option value="sim_rig">Workstation (Sim Rig)</option>
          <option value="edge_kit">Edge Kit (Jetson)</option>
        </select>
      </div>

      {/* Workstation GPU Fields */}
      {formData.hardware_type === 'sim_rig' && (
        <>
          <div className="form-group margin-bottom--lg">
            <label className="form-label" htmlFor="gpu_model">
              Workstation GPU
            </label>
            <select
              id="gpu_model"
              name="gpu_model"
              value={formData.gpu_model}
              onChange={handleChange}
              className="form-select glass-input"
              required
            >
              <option value="">Select GPU...</option>
              {WORKSTATION_OPTIONS.map(option => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
          </div>

          <div className="form-group margin-bottom--lg">
            <label className="form-label" htmlFor="gpu_vram_gb">
              GPU VRAM (GB)
            </label>
            <select
              id="gpu_vram_gb"
              name="gpu_vram_gb"
              value={formData.gpu_vram_gb}
              onChange={handleChange}
              className="form-select glass-input"
              required
            >
              <option value="12">12 GB</option>
              <option value="16">16 GB</option>
              <option value="24">24 GB</option>
              <option value="32">32 GB</option>
            </select>
          </div>
        </>
      )}

      {/* Edge Kit Fields */}
      {formData.hardware_type === 'edge_kit' && (
        <div className="form-group margin-bottom--lg">
          <label className="form-label" htmlFor="edge_kit_type">
            Edge Device
          </label>
          <select
            id="edge_kit_type"
            name="edge_kit_type"
            value={formData.edge_kit_type}
            onChange={handleChange}
            className="form-select glass-input"
            required
          >
            <option value="">Select Edge Device...</option>
            {EDGE_KIT_OPTIONS.map(option => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        </div>
      )}

      {/* Robot Selection */}
      <div className="form-group margin-bottom--lg">
        <label className="form-label" htmlFor="robot_model">
          Robot Platform
        </label>
        <select
          id="robot_model"
          name="robot_model"
          value={formData.robot_model}
          onChange={handleChange}
          className="form-select glass-input"
        >
          <option value="">Select Robot (Optional)...</option>
          {ROBOT_OPTIONS.map(option => (
            <option key={option.value} value={option.value}>
              {option.label}
            </option>
          ))}
        </select>
      </div>

      {/* Status Messages */}
      {error && (
        <div className="alert alert--danger margin-bottom--md" role="alert">
          {error}
        </div>
      )}

      {saveStatus && (
        <div
          className={clsx(
            'alert margin-bottom--md',
            saveStatus.type === 'success' ? 'alert--success' : 'alert--danger'
          )}
          role="alert"
        >
          {saveStatus.message}
        </div>
      )}

      {/* Submit Button */}
      <div className="text--center margin-top--lg">
        <button
          type="submit"
          className="button button--primary button--lg neon-button"
          disabled={saving}
        >
          {saving ? (
            <>
              <span className="spinner spinner--sm margin-right--sm"></span>
              Saving...
            </>
          ) : (
            'Save Configuration'
          )}
        </button>
      </div>
    </form>
  );
}
