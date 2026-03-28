/**
 * Personalization context for Phase 7 - Final Intelligence.
 * 
 * Manages user hardware profile, skill level, and language preferences.
 * Persists to localStorage and syncs with backend API.
 */

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import axios from 'axios';

// Types
export type SkillLevel = 'beginner' | 'intermediate' | 'advanced';
export type HardwareType = 'sim_rig' | 'edge_kit' | 'unitree';
export type LanguageCode = 'en' | 'ur-Latn';

export interface HardwareProfile {
  id?: string;
  hardware_type: HardwareType;
  gpu_model?: string;
  gpu_vram_gb?: number;
  ubuntu_version?: string;
  edge_kit_type?: string;
  jetpack_version?: string;
  robot_model?: string;
}

export interface UserProfile {
  user_id: string;
  email: string;
  skill_level: SkillLevel;
  display_name?: string;
  hardware_config?: HardwareProfile;
}

interface PersonalizationContextType {
  // User profile
  userProfile: UserProfile | null;
  isLoading: boolean;
  
  // Hardware profile
  hardwareProfile: HardwareProfile | null;
  
  // Skill level
  skillLevel: SkillLevel;
  
  // Language preference
  language: LanguageCode;
  
  // Personalization toggle
  personalizationEnabled: boolean;
  
  // Actions
  setLanguage: (lang: LanguageCode) => void;
  setPersonalizationEnabled: (enabled: boolean) => void;
  updateHardwareProfile: (profile: HardwareProfile) => Promise<void>;
  updateSkillLevel: (level: SkillLevel) => Promise<void>;
  refreshProfile: () => Promise<void>;
}

const PersonalizationContext = createContext<PersonalizationContextType | undefined>(undefined);

const API_BASE_URL = 'http://localhost:8000/api/v1';

export function PersonalizationProvider({ children }: { children: ReactNode }) {
  const [userProfile, setUserProfile] = useState<UserProfile | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [language, setLanguageState] = useState<LanguageCode>('en');
  const [personalizationEnabled, setPersonalizationEnabledState] = useState(true);

  // Load initial state from localStorage and backend
  useEffect(() => {
    const initializeState = async () => {
      // Load language preference from localStorage
      const savedLanguage = localStorage.getItem('language') as LanguageCode;
      if (savedLanguage && ['en', 'ur-Latn'].includes(savedLanguage)) {
        setLanguageState(savedLanguage);
      }

      // Load personalization toggle state
      const savedEnabled = localStorage.getItem('personalizationEnabled');
      if (savedEnabled !== null) {
        setPersonalizationEnabledState(savedEnabled === 'true');
      }

      // Try to load user profile from backend
      try {
        const token = localStorage.getItem('access_token');
        if (token) {
          const response = await axios.get(`${API_BASE_URL}/user-profile`, {
            headers: { Authorization: `Bearer ${token}` },
          });
          setUserProfile(response.data);
        }
      } catch (error) {
        console.log('Could not load user profile (may not be authenticated)');
      } finally {
        setIsLoading(false);
      }
    };

    initializeState();
  }, []);

  // Set language and persist to localStorage
  const setLanguage = (lang: LanguageCode) => {
    setLanguageState(lang);
    localStorage.setItem('language', lang);
  };

  // Toggle personalization and persist
  const setPersonalizationEnabled = (enabled: boolean) => {
    setPersonalizationEnabledState(enabled);
    localStorage.setItem('personalizationEnabled', enabled.toString());
  };

  // Update hardware profile via API
  const updateHardwareProfile = async (profile: HardwareProfile) => {
    const token = localStorage.getItem('access_token');
    if (!token) {
      throw new Error('Not authenticated');
    }

    await axios.put(`${API_BASE_URL}/user-profile/hardware-config`, profile, {
      headers: { Authorization: `Bearer ${token}` },
    });

    // Refresh profile
    await refreshProfile();
  };

  // Update skill level via API
  const updateSkillLevel = async (level: SkillLevel) => {
    const token = localStorage.getItem('access_token');
    if (!token) {
      throw new Error('Not authenticated');
    }

    await axios.put(`${API_BASE_URL}/user-profile`, { skill_level: level }, {
      headers: { Authorization: `Bearer ${token}` },
    });

    // Refresh profile
    await refreshProfile();
  };

  // Refresh user profile from backend
  const refreshProfile = async () => {
    const token = localStorage.getItem('access_token');
    if (!token) {
      return;
    }

    try {
      const response = await axios.get(`${API_BASE_URL}/user-profile`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setUserProfile(response.data);
    } catch (error) {
      console.error('Failed to refresh profile:', error);
    }
  };

  // Derived values
  const hardwareProfile = userProfile?.hardware_config || null;
  const skillLevel = userProfile?.skill_level || 'beginner';

  return (
    <PersonalizationContext.Provider
      value={{
        userProfile,
        isLoading,
        hardwareProfile,
        skillLevel,
        language,
        personalizationEnabled,
        setLanguage,
        setPersonalizationEnabled,
        updateHardwareProfile,
        updateSkillLevel,
        refreshProfile,
      }}
    >
      {children}
    </PersonalizationContext.Provider>
  );
}

export function usePersonalization(): PersonalizationContextType {
  const context = useContext(PersonalizationContext);
  if (!context) {
    throw new Error('usePersonalization must be used within PersonalizationProvider');
  }
  return context;
}
