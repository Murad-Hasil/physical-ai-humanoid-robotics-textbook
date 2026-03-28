/**
 * Hardware Context for managing user's hardware profile globally.
 * 
 * Provides hardware state and sync functions across the application.
 */

import { createContext, useContext, useState, useEffect } from 'react';
import { useAuth } from '../hooks/useAuth';
import axios from 'axios';

// Webpack 5 does not polyfill process. Using hardcoded dev URL.
const API_BASE_URL = 'http://localhost:8000';

// Hardware Context
const HardwareContext = createContext(null);

/**
 * Hardware Provider component
 */
export function HardwareProvider({ children }) {
  const { user, loading: authLoading } = useAuth();
  const [hardwareProfile, setHardwareProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  /**
   * Fetch hardware profile from backend
   */
  async function fetchHardwareProfile() {
    try {
      const token = localStorage.getItem('access_token');
      if (!token) {
        setHardwareProfile(null);
        setLoading(false);
        return;
      }

      const response = await axios.get(
        `${API_BASE_URL}/api/v1/user-profile/hardware-config`,
        {
          headers: {
            'Authorization': `Bearer ${token}`,
          },
        }
      );

      setHardwareProfile(response.data);
      setError(null);
    } catch (err) {
      if (err.response?.status === 404) {
        // No hardware profile set - this is OK
        setHardwareProfile(null);
      } else {
        console.error('Failed to fetch hardware profile:', err);
        setError(err.message);
      }
    } finally {
      setLoading(false);
    }
  }

  /**
   * Update hardware profile
   */
  async function updateHardwareProfile(profileData) {
    try {
      setError(null);
      const token = localStorage.getItem('access_token');
      
      const response = await axios.put(
        `${API_BASE_URL}/api/v1/user-profile/hardware-config`,
        profileData,
        {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        }
      );

      setHardwareProfile(response.data);
      return { success: true, data: response.data };
    } catch (err) {
      console.error('Failed to update hardware profile:', err);
      setError(err.response?.data?.detail?.message || err.message);
      return { 
        success: false, 
        error: err.response?.data?.detail?.message || err.message 
      };
    }
  }

  /**
   * Get display string for hardware
   */
  function getHardwareDisplayString() {
    if (!hardwareProfile) return 'Not Configured';
    
    if (hardwareProfile.hardware_type === 'edge_kit') {
      return hardwareProfile.edge_kit_type || 'Edge Kit';
    } else if (hardwareProfile.hardware_type === 'sim_rig') {
      return hardwareProfile.gpu_model || 'Sim Rig';
    }
    
    return 'Custom Setup';
  }

  // Fetch hardware profile when user authenticates
  useEffect(() => {
    if (user && !authLoading) {
      fetchHardwareProfile();
    } else if (!user) {
      setHardwareProfile(null);
      setLoading(false);
    }
  }, [user, authLoading]);

  const value = {
    hardwareProfile,
    loading,
    error,
    updateHardwareProfile,
    fetchHardwareProfile,
    getHardwareDisplayString,
  };

  return (
    <HardwareContext.Provider value={value}>
      {children}
    </HardwareContext.Provider>
  );
}

/**
 * Use hardware context hook
 */
export function useHardware() {
  const context = useContext(HardwareContext);
  if (!context) {
    throw new Error('useHardware must be used within a HardwareProvider');
  }
  return context;
}
