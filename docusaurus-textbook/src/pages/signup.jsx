/**
 * Signup Page — with Hardware Onboarding (T025)
 *
 * Multi-step registration:
 *   Step 1: Email + Password
 *   Step 2: Skill Level selection
 *   Step 3: Hardware Profile configuration
 */

import React, { useState } from 'react';
import Layout from '@theme/Layout';
import { useAuth } from '@site/src/hooks/useAuth';
import { SkillLevelSelector } from '@site/src/components/onboarding/SkillLevelSelector';
import HardwareProfileForm from '@site/src/components/onboarding/HardwareProfileForm';

const API_BASE_URL = 'https://mb-murad-physical-ai-backend.hf.space';

export default function Signup() {
  const { register, error: authError } = useAuth();

  // Step: 1 = credentials, 2 = skill level, 3 = hardware
  const [step, setStep] = useState(1);

  const [formData, setFormData] = useState({
    email: '',
    password: '',
    confirmPassword: '',
  });
  const [skillLevel, setSkillLevel] = useState('beginner');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    setError('');
  };

  // Step 1: Validate credentials and move to step 2
  const handleCredentialsSubmit = (e) => {
    e.preventDefault();
    setError('');

    if (formData.password !== formData.confirmPassword) {
      setError('Passwords do not match');
      return;
    }
    if (formData.password.length < 8) {
      setError('Password must be at least 8 characters long');
      return;
    }
    setStep(2);
  };

  // Step 2: Save skill level and move to step 3
  const handleSkillSubmit = (e) => {
    e.preventDefault();
    setStep(3);
  };

  // Step 3: Register account + save skill level + hardware config
  const handleHardwareSubmit = async (hardwareData) => {
    setLoading(true);
    setError('');

    try {
      // Register account
      await register(formData.email, formData.password);

      // Save skill level + hardware config using the access_token just set
      const token = localStorage.getItem('access_token');
      if (token) {
        // Save skill level
        await fetch(`${API_BASE_URL}/api/v1/user-profile`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
          },
          body: JSON.stringify({ skill_level: skillLevel }),
        });

        // Save hardware config
        await fetch(`${API_BASE_URL}/api/v1/user-profile/hardware-config`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
          },
          body: JSON.stringify(hardwareData),
        });
      }

      window.location.href = '/physical-ai-humanoid-robotics-textbook/profile';
    } catch (err) {
      setError(err.message || 'Registration failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  // Step indicator
  const steps = ['Account', 'Skill Level', 'Hardware'];

  return (
    <Layout
      title="Sign Up"
      description="Create your Physical AI account with hardware profile"
    >
      <main className="container margin-vert--xl">
        <div className="row">
          <div className="col col--8 col--offset-2">

            {/* Step Indicator */}
            <div style={{ display: 'flex', justifyContent: 'center', gap: '2rem', marginBottom: '2rem' }}>
              {steps.map((label, i) => (
                <div key={i} style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                  <div style={{
                    width: '2rem',
                    height: '2rem',
                    borderRadius: '50%',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    fontSize: '0.875rem',
                    fontWeight: 'bold',
                    background: step > i + 1 ? '#00F3FF' : step === i + 1 ? 'rgba(0,243,255,0.2)' : 'rgba(255,255,255,0.1)',
                    border: `2px solid ${step >= i + 1 ? '#00F3FF' : 'rgba(255,255,255,0.2)'}`,
                    color: step > i + 1 ? '#000' : '#00F3FF',
                  }}>
                    {step > i + 1 ? '✓' : i + 1}
                  </div>
                  <span style={{ color: step >= i + 1 ? '#00F3FF' : '#888', fontSize: '0.875rem' }}>
                    {label}
                  </span>
                  {i < steps.length - 1 && (
                    <div style={{ width: '3rem', height: '1px', background: step > i + 1 ? '#00F3FF' : 'rgba(255,255,255,0.2)' }} />
                  )}
                </div>
              ))}
            </div>

            <div className="glass-card padding--xl" style={{
              background: 'rgba(15, 23, 42, 0.5)',
              backdropFilter: 'blur(12px)',
              border: '1px solid rgba(0, 243, 255, 0.2)',
              borderRadius: '12px',
            }}>

              {/* ── STEP 1: Credentials ── */}
              {step === 1 && (
                <>
                  <div className="text--center margin-bottom--xl">
                    <h1 className="neon-text" style={{ fontSize: '2.5rem' }}>Create Account</h1>
                    <p style={{ color: '#aaa', marginTop: '0.5rem' }}>
                      Join the Physical AI curriculum
                    </p>
                  </div>

                  <form onSubmit={handleCredentialsSubmit}>
                    {['email', 'password', 'confirmPassword'].map((field) => (
                      <div key={field} className="margin-bottom--lg">
                        <label style={{ display: 'block', marginBottom: '0.5rem', color: '#00FFFF', fontWeight: 600 }}>
                          {field === 'email' ? 'Email Address' : field === 'password' ? 'Password' : 'Confirm Password'}
                        </label>
                        <input
                          type={field === 'email' ? 'email' : 'password'}
                          name={field}
                          value={formData[field]}
                          onChange={handleChange}
                          style={{
                            width: '100%', padding: '0.75rem 1rem',
                            background: 'rgba(15, 23, 42, 0.6)',
                            border: '1px solid rgba(0, 243, 255, 0.3)',
                            borderRadius: '0.5rem', color: '#fff', fontSize: '1rem',
                          }}
                          placeholder={field === 'email' ? 'you@example.com' : '••••••••'}
                          minLength={field !== 'email' ? 8 : undefined}
                          required
                        />
                      </div>
                    ))}

                    {(error || authError) && (
                      <div className="alert alert--danger margin-bottom--lg" role="alert">
                        {error || authError}
                      </div>
                    )}

                    <button type="submit" className="button button--primary button--block" style={{
                      background: 'rgba(0,243,255,0.1)', border: '2px solid #00F3FF',
                      color: '#00F3FF', padding: '0.875rem', fontSize: '1rem', fontWeight: 600,
                    }}>
                      Next: Choose Skill Level →
                    </button>

                    <div className="text--center margin-top--lg">
                      <p style={{ color: '#aaa' }}>
                        Already have an account?{' '}
                        <a href="/physical-ai-humanoid-robotics-textbook/login" style={{ color: '#00F3FF' }}>Sign in</a>
                      </p>
                    </div>
                  </form>
                </>
              )}

              {/* ── STEP 2: Skill Level ── */}
              {step === 2 && (
                <>
                  <div className="text--center margin-bottom--xl">
                    <h2 style={{ color: '#00F3FF', fontSize: '1.75rem' }}>What's your experience level?</h2>
                    <p style={{ color: '#aaa' }}>This helps us personalize your learning content</p>
                  </div>

                  <form onSubmit={handleSkillSubmit}>
                    <SkillLevelSelector
                      value={skillLevel}
                      onChange={setSkillLevel}
                      showDescriptions
                      direction="vertical"
                    />

                    <div style={{ display: 'flex', gap: '1rem', marginTop: '2rem' }}>
                      <button
                        type="button"
                        onClick={() => setStep(1)}
                        style={{
                          flex: 1, padding: '0.875rem',
                          background: 'transparent', border: '1px solid rgba(255,255,255,0.2)',
                          color: '#aaa', borderRadius: '0.5rem', cursor: 'pointer',
                        }}
                      >
                        ← Back
                      </button>
                      <button type="submit" style={{
                        flex: 2, padding: '0.875rem',
                        background: 'rgba(0,243,255,0.1)', border: '2px solid #00F3FF',
                        color: '#00F3FF', borderRadius: '0.5rem', fontWeight: 600, cursor: 'pointer',
                      }}>
                        Next: Configure Hardware →
                      </button>
                    </div>
                  </form>
                </>
              )}

              {/* ── STEP 3: Hardware Profile ── */}
              {step === 3 && (
                <>
                  <div className="text--center margin-bottom--xl">
                    <h2 style={{ color: '#00F3FF', fontSize: '1.75rem' }}>Your Hardware Setup</h2>
                    <p style={{ color: '#aaa' }}>Content will adapt based on your hardware capabilities</p>
                  </div>

                  {error && (
                    <div className="alert alert--danger margin-bottom--lg" role="alert">{error}</div>
                  )}

                  <HardwareProfileForm
                    onSubmit={handleHardwareSubmit}
                    isLoading={loading}
                  />

                  <button
                    type="button"
                    onClick={() => setStep(2)}
                    style={{
                      width: '100%', marginTop: '1rem', padding: '0.75rem',
                      background: 'transparent', border: '1px solid rgba(255,255,255,0.2)',
                      color: '#aaa', borderRadius: '0.5rem', cursor: 'pointer',
                    }}
                  >
                    ← Back to Skill Level
                  </button>
                </>
              )}

            </div>
          </div>
        </div>
      </main>
    </Layout>
  );
}
