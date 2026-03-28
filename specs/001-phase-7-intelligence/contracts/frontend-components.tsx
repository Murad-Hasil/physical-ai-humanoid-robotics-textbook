# Frontend Component Contracts: Phase 7 Final Intelligence

**Created**: 2026-03-26
**Feature**: 001-phase-7-intelligence
**Purpose**: Define TypeScript interfaces and component contracts for React components

---

## Context Provider

### PersonalizationContext

**Location**: `docusaurus-textbook/src/context/PersonalizationContext.tsx`

```typescript
import React, { createContext, useContext, useState, useEffect } from 'react';

export type SkillLevel = 'beginner' | 'intermediate' | 'advanced';
export type HardwareType = 'sim_rig' | 'edge_kit' | 'unitree';
export type LanguageCode = 'en' | 'ur-Latn';

export interface HardwareProfile {
  id: string;
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
  refreshProfile: () => Promise<void>;
}

export const PersonalizationContext = createContext<PersonalizationContextType | undefined>(undefined);

export function usePersonalization(): PersonalizationContextType {
  const context = useContext(PersonalizationContext);
  if (!context) {
    throw new Error('usePersonalization must be used within PersonalizationProvider');
  }
  return context;
}
```

**Usage Example**:
```typescript
// In any component
const { 
  hardwareProfile, 
  skillLevel, 
  language, 
  setLanguage,
  personalizationEnabled 
} = usePersonalization();

// Show hardware-specific UI
if (hardwareProfile?.hardware_type === 'edge_kit') {
  return <EdgeOptimizedContent />;
}
```

---

## Onboarding Components

### HardwareProfileForm

**Location**: `docusaurus-textbook/src/components/onboarding/HardwareProfileForm.tsx`

```typescript
import React from 'react';

export interface HardwareProfileFormProps {
  onSubmit: (data: HardwareProfileFormData) => Promise<void>;
  initialValues?: Partial<HardwareProfileFormData>;
  isLoading?: boolean;
}

export interface HardwareProfileFormData {
  hardware_type: 'sim_rig' | 'edge_kit' | 'unitree';
  gpu_model?: string;
  gpu_vram_gb?: number;
  ubuntu_version?: string;
  edge_kit_type?: string;
  jetpack_version?: string;
  robot_model?: string;
}

export const HardwareProfileForm: React.FC<HardwareProfileFormProps> = ({
  onSubmit,
  initialValues,
  isLoading = false,
}) => {
  // Implementation
};

export default HardwareProfileForm;
```

**Usage Example**:
```typescript
<HardwareProfileForm
  onSubmit={async (data) => {
    await api.updateHardwareConfig(data);
    showToast('Hardware profile saved!');
  }}
  initialValues={{
    hardware_type: 'sim_rig',
    gpu_model: 'RTX 4070 Ti',
  }}
/>
```

---

### SkillLevelSelector

**Location**: `docusaurus-textbook/src/components/onboarding/SkillLevelSelector.tsx`

```typescript
import React from 'react';

export interface SkillLevelSelectorProps {
  value: 'beginner' | 'intermediate' | 'advanced';
  onChange: (level: 'beginner' | 'intermediate' | 'advanced') => void;
  disabled?: boolean;
  showDescriptions?: boolean;
}

export const SkillLevelSelector: React.FC<SkillLevelSelectorProps> = ({
  value,
  onChange,
  disabled = false,
  showDescriptions = true,
}) => {
  // Implementation
};

export default SkillLevelSelector;
```

**Skill Level Descriptions**:
- **Beginner**: "New to Physical AI. I want foundational concepts and step-by-step guidance."
- **Intermediate**: "Some experience with AI/robotics. I understand basic concepts and want technical details."
- **Advanced**: "Experienced practitioner. I want optimization strategies and production considerations."

---

## Personalization Components

### PersonalizationToggle

**Location**: `docusaurus-textbook/src/components/personalization/PersonalizationToggle.tsx`

```typescript
import React from 'react';

export interface PersonalizationToggleProps {
  enabled: boolean;
  onToggle: (enabled: boolean) => void;
  size?: 'sm' | 'md' | 'lg';
}

export const PersonalizationToggle: React.FC<PersonalizationToggleProps> = ({
  enabled,
  onToggle,
  size = 'md',
}) => {
  // Implementation
};

export default PersonalizationToggle;
```

---

### HardwareIndicator

**Location**: `docusaurus-textbook/src/components/personalization/HardwareIndicator.tsx`

```typescript
import React from 'react';

export interface HardwareIndicatorProps {
  hardwareProfile: HardwareProfile;
  skillLevel: SkillLevel;
  onEdit?: () => void;
  compact?: boolean;
}

export const HardwareIndicator: React.FC<HardwareIndicatorProps> = ({
  hardwareProfile,
  skillLevel,
  onEdit,
  compact = false,
}) => {
  // Implementation
};

export default HardwareIndicator;
```

**Visual Design**:
- Show hardware icon (desktop GPU / Jetson / robot)
- Display: "RTX 4070 Ti • Advanced" or "Jetson Orin Nano • Beginner"
- Click to edit (triggers profile modal)
- Glassmorphism styling with neon accent

---

## Translation Components

### TranslationToggle

**Location**: `docusaurus-textbook/src/components/translation/TranslationToggle.tsx`

```typescript
import React from 'react';

export interface TranslationToggleProps {
  chapterId: string;
  currentLang: 'en' | 'ur-Latn';
  onToggle: (newLang: 'en' | 'ur-Latn') => void;
  translationAvailable?: boolean;
  isLoading?: boolean;
}

export const TranslationToggle: React.FC<TranslationToggleProps> = ({
  chapterId,
  currentLang,
  onToggle,
  translationAvailable = true,
  isLoading = false,
}) => {
  // Implementation
};

export default TranslationToggle;
```

**Visual Design**:
- Toggle switch with "EN" / "اردو" labels
- Neon glow when active
- Disabled state if translation not available
- Tooltip: "Switch to Roman Urdu" / "Switch to English"

---

### TranslationProgress

**Location**: `docusaurus-textbook/src/components/translation/TranslationProgress.tsx`

```typescript
import React from 'react';

export interface TranslationProgressProps {
  status: 'draft' | 'in_review' | 'published';
  compact?: boolean;
}

export const TranslationProgress: React.FC<TranslationProgressProps> = ({
  status,
  compact = false,
}) => {
  // Implementation
};

export default TranslationProgress;
```

**Visual Design**:
- **Draft**: Yellow indicator with "AI Translation in progress"
- **In Review**: Orange indicator with "Under review"
- **Published**: Green checkmark
- Compact mode: Icon only
- Full mode: Icon + text label

---

## Page Components

### Signup Page

**Location**: `docusaurus-textbook/src/pages/signup.tsx`

```typescript
import React from 'react';
import HardwareProfileForm from '../components/onboarding/HardwareProfileForm';
import SkillLevelSelector from '../components/onboarding/SkillLevelSelector';

interface SignupFormData {
  email: string;
  password: string;
  skill_level: 'beginner' | 'intermediate' | 'advanced';
  hardware_config?: HardwareProfileFormData;
}

export const SignupPage: React.FC = () => {
  const handleSubmit = async (data: SignupFormData) => {
    // Create account with hardware profile
  };

  return (
    <div className="cyber-signup-container">
      <h1>Join Physical AI Curriculum</h1>
      
      {/* Email/Password */}
      {/* Hardware Profile Form */}
      {/* Skill Level Selector */}
      {/* Submit Button */}
    </div>
  );
};

export default SignupPage;
```

---

### Profile Page

**Location**: `docusaurus-textbook/src/pages/profile.tsx`

```typescript
import React from 'react';
import { usePersonalization } from '../context/PersonalizationContext';
import HardwareProfileForm from '../components/onboarding/HardwareProfileForm';
import SkillLevelSelector from '../components/onboarding/SkillLevelSelector';

export const ProfilePage: React.FC = () => {
  const { userProfile, refreshProfile } = usePersonalization();

  const handleUpdate = async (data) => {
    await api.updateProfile(data);
    await refreshProfile();
  };

  return (
    <div className="cyber-profile-container">
      <h1>Your Profile</h1>
      
      {/* Current Hardware Display */}
      <HardwareIndicator 
        hardwareProfile={userProfile.hardware_config}
        skillLevel={userProfile.skill_level}
      />
      
      {/* Edit Hardware Form */}
      <HardwareProfileForm onSubmit={handleUpdate} />
      
      {/* Edit Skill Level */}
      <SkillLevelSelector 
        value={userProfile.skill_level}
        onChange={(level) => handleUpdate({ skill_level: level })}
      />
    </div>
  );
};

export default ProfilePage;
```

---

## Theme Customization

### DocItem Wrapper

**Location**: `docusaurus-textbook/src/theme/DocItem/index.tsx`

```typescript
import React from 'react';
import OriginalDocItem from '@theme-original/DocItem';
import { usePersonalization } from '@site/src/context/PersonalizationContext';
import TranslationToggle from '@site/src/components/translation/TranslationToggle';
import PersonalizedSummary from '@site/src/components/personalization/PersonalizedSummary';
import HardwareIndicator from '@site/src/components/personalization/HardwareIndicator';

export default function DocItem(props: any) {
  const { 
    language, 
    setLanguage, 
    personalizationEnabled,
    hardwareProfile,
    skillLevel 
  } = usePersonalization();

  const chapterId = props.content.metadata.id;

  return (
    <OriginalDocItem
      {...props}
      header={
        <>
          {/* Hardware Profile Indicator */}
          {personalizationEnabled && hardwareProfile && (
            <HardwareIndicator
              hardwareProfile={hardwareProfile}
              skillLevel={skillLevel}
              compact
            />
          )}
          
          {/* Translation Toggle */}
          <TranslationToggle
            chapterId={chapterId}
            currentLang={language}
            onToggle={setLanguage}
          />
        </>
      }
      content={
        personalizationEnabled ? (
          <PersonalizedSummary chapterId={chapterId} />
        ) : null
      }
    />
  );
}
```

---

## API Service Layer

### personalization.ts

**Location**: `docusaurus-textbook/src/services/personalization.ts`

```typescript
import api from './api';

export interface PersonalizationService {
  getUserProfile(): Promise<UserProfile>;
  updateProfile(data: StudentProfileUpdate): Promise<UserProfile>;
  updateHardwareConfig(data: HardwareProfileFormData): Promise<HardwareProfile>;
  getChapterSummary(
    chapterId: string,
    hardwareProfile?: HardwareType,
    skillLevel?: SkillLevel
  ): Promise<ChapterSummary>;
  regenerateSummaries(
    hardwareProfile?: HardwareType,
    skillLevel?: SkillLevel
  ): Promise<JobStatus>;
}

export const personalizationService: PersonalizationService = {
  async getUserProfile() {
    const response = await api.get('/user-profile');
    return response.data;
  },

  async updateProfile(data) {
    const response = await api.put('/user-profile', data);
    return response.data;
  },

  async updateHardwareConfig(data) {
    const response = await api.put('/user-profile/hardware-config', data);
    return response.data;
  },

  async getChapterSummary(chapterId, hardwareProfile, skillLevel) {
    const params = new URLSearchParams();
    if (hardwareProfile) params.append('hardware_profile', hardwareProfile);
    if (skillLevel) params.append('skill_level', skillLevel);
    
    const response = await api.get(`/chapters/${chapterId}/summary?${params}`);
    return response.data;
  },

  async regenerateSummaries(hardwareProfile, skillLevel) {
    const response = await api.post('/personalization/regenerate', {
      hardware_profile: hardwareProfile,
      skill_level: skillLevel,
    });
    return response.data;
  },
};
```

---

### translations.ts

**Location**: `docusaurus-textbook/src/services/translations.ts`

```typescript
import api from './api';

export interface TranslationService {
  getTranslation(
    chapterId: string,
    languageCode: string
  ): Promise<Translation>;
  updateTranslation(
    chapterId: string,
    data: TranslationUpdateData
  ): Promise<Translation>;
  getTranslationStats(): Promise<TranslationStats>;
}

export const translationService: TranslationService = {
  async getTranslation(chapterId, languageCode) {
    const response = await api.get(
      `/chapters/${chapterId}/translation?lang=${languageCode}`
    );
    return response.data;
  },

  async updateTranslation(chapterId, data) {
    const response = await api.put(
      `/chapters/${chapterId}/translation`,
      data
    );
    return response.data;
  },

  async getTranslationStats() {
    const response = await api.get('/translations/status');
    return response.data;
  },
};
```

---

## Styling Guidelines

All components must follow the "Robotic SaaS" glassmorphism theme:

```css
/* From custom.css */
.glass-panel {
  background: rgba(10, 10, 20, 0.7);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(0, 243, 255, 0.2);
  box-shadow: 0 8px 32px rgba(0, 243, 255, 0.1);
}

.neon-border {
  border: 2px solid #00F3FF;
  box-shadow: 0 0 10px #00F3FF, inset 0 0 10px rgba(0, 243, 255, 0.1);
}

.cyber-button {
  background: linear-gradient(135deg, rgba(0, 243, 255, 0.2), rgba(255, 107, 53, 0.2));
  border: 1px solid #00F3FF;
  color: #00F3FF;
  transition: all 0.3s ease;
}

.cyber-button:hover {
  box-shadow: 0 0 20px rgba(0, 243, 255, 0.5);
  transform: translateY(-2px);
}

/* Animation for translation toggle */
@keyframes pulse-cyan {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.translation-in-progress {
  animation: pulse-cyan 2s infinite;
  color: #FFD700; /* Gold for "in progress" */
}
```

---

## Testing Guidelines

### Component Tests

```typescript
// __tests__/HardwareProfileForm.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import HardwareProfileForm from '../components/onboarding/HardwareProfileForm';

describe('HardwareProfileForm', () => {
  it('submits valid hardware configuration', async () => {
    const mockSubmit = jest.fn();
    render(<HardwareProfileForm onSubmit={mockSubmit} />);
    
    fireEvent.change(screen.getByLabelText(/hardware type/i), {
      target: { value: 'sim_rig' }
    });
    
    fireEvent.click(screen.getByRole('button', { name: /save/i }));
    
    await waitFor(() => {
      expect(mockSubmit).toHaveBeenCalledWith(
        expect.objectContaining({
          hardware_type: 'sim_rig'
        })
      );
    });
  });
});
```

### Context Tests

```typescript
// __tests__/PersonalizationContext.test.tsx
import { renderHook, act } from '@testing-library/react';
import { PersonalizationProvider, usePersonalization } from '../context/PersonalizationContext';

describe('PersonalizationContext', () => {
  it('persists language preference', () => {
    const wrapper = ({ children }) => (
      <PersonalizationProvider>{children}</PersonalizationProvider>
    );
    
    const { result } = renderHook(() => usePersonalization(), { wrapper });
    
    act(() => {
      result.current.setLanguage('ur-Latn');
    });
    
    expect(localStorage.getItem('language')).toBe('ur-Latn');
    expect(result.current.language).toBe('ur-Latn');
  });
});
```

---

## Next Steps

1. Implement context provider with localStorage sync
2. Build onboarding components (HardwareProfileForm, SkillLevelSelector)
3. Build personalization components (Toggle, HardwareIndicator)
4. Build translation components (Toggle, Progress indicator)
5. Swizzle Docusaurus DocItem component
6. Integrate with signup/profile pages
7. Write component and integration tests
