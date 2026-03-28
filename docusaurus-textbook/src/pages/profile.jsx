/**
 * Profile Page — Hardware Dashboard (T026)
 *
 * Shows current hardware profile + skill level,
 * allows editing both via HardwareProfileForm & SkillLevelSelector.
 */

import React, { useState } from 'react';
import Layout from '@theme/Layout';
import { useAuth } from '@site/src/hooks/useAuth';
import AuthGuard from '@site/src/components/AuthGuard';
import { usePersonalization } from '@site/src/context/PersonalizationContext';
import HardwareProfileForm from '@site/src/components/onboarding/HardwareProfileForm';
import { SkillLevelSelector } from '@site/src/components/onboarding/SkillLevelSelector';
import HardwareIndicator from '@site/src/components/personalization/HardwareIndicator';

export default function Profile() {
  const { user } = useAuth();
  const { skillLevel, hardwareProfile, updateSkillLevel, updateHardwareProfile, isLoading } = usePersonalization();

  const [editingHardware, setEditingHardware] = useState(false);
  const [editingSkill, setEditingSkill] = useState(false);
  const [localSkill, setLocalSkill] = useState(skillLevel);
  const [saving, setSaving] = useState(false);
  const [successMsg, setSuccessMsg] = useState('');

  const handleSkillSave = async (e) => {
    e.preventDefault();
    setSaving(true);
    try {
      await updateSkillLevel(localSkill);
      setSuccessMsg('Skill level updated!');
      setEditingSkill(false);
      setTimeout(() => setSuccessMsg(''), 3000);
    } catch (err) {
      console.error(err);
    } finally {
      setSaving(false);
    }
  };

  const handleHardwareSave = async (data) => {
    setSaving(true);
    try {
      await updateHardwareProfile(data);
      setSuccessMsg('Hardware profile updated!');
      setEditingHardware(false);
      setTimeout(() => setSuccessMsg(''), 3000);
    } catch (err) {
      console.error(err);
    } finally {
      setSaving(false);
    }
  };

  return (
    <AuthGuard>
      <Layout title="Hardware Dashboard" description="Your personalized hardware profile">
        <main className="container margin-vert--lg">
          <div className="row">
            <div className="col col--8 col--offset-2">

              {/* Header */}
              <div className="text--center margin-bottom--xl">
                <h1 className="neon-text" style={{ fontSize: '2.5rem' }}>🖥️ Hardware Dashboard</h1>
                {user && (
                  <div style={{
                    display: 'inline-flex', alignItems: 'center', gap: '0.5rem',
                    padding: '0.4rem 1rem', marginTop: '0.75rem',
                    background: 'rgba(0,243,255,0.08)', border: '1px solid rgba(0,243,255,0.3)',
                    borderRadius: '20px', fontSize: '0.9rem',
                  }}>
                    <span style={{ width: 8, height: 8, borderRadius: '50%', background: '#00F3FF', boxShadow: '0 0 8px #00F3FF' }} />
                    <span style={{ color: '#aaa' }}>Logged in as</span>
                    <strong style={{ color: '#00F3FF' }}>{user.email}</strong>
                  </div>
                )}
              </div>

              {/* Success message */}
              {successMsg && (
                <div className="alert alert--success margin-bottom--lg" role="alert">
                  ✅ {successMsg}
                </div>
              )}

              {isLoading ? (
                <div className="text--center" style={{ color: '#aaa', padding: '2rem' }}>Loading profile...</div>
              ) : (
                <>
                  {/* ── Current Hardware Status ── */}
                  <div className="glass-card padding--lg margin-bottom--lg" style={{
                    background: 'rgba(15,23,42,0.5)', backdropFilter: 'blur(12px)',
                    border: '1px solid rgba(0,243,255,0.2)', borderRadius: '12px',
                  }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
                      <h2 style={{ color: '#00F3FF', margin: 0 }}>Current Setup</h2>
                      <button
                        onClick={() => { setEditingHardware(!editingHardware); setEditingSkill(false); }}
                        style={{
                          padding: '0.4rem 1rem', background: 'rgba(0,243,255,0.1)',
                          border: '1px solid #00F3FF', borderRadius: '8px',
                          color: '#00F3FF', cursor: 'pointer', fontSize: '0.875rem',
                        }}
                      >
                        {editingHardware ? '✕ Cancel' : '✏️ Edit Hardware'}
                      </button>
                    </div>

                    {hardwareProfile ? (
                      <HardwareIndicator />
                    ) : (
                      <p style={{ color: '#888' }}>No hardware profile configured yet. Click "Edit Hardware" to set up.</p>
                    )}

                    {editingHardware && (
                      <div style={{ marginTop: '1.5rem', borderTop: '1px solid rgba(0,243,255,0.2)', paddingTop: '1.5rem' }}>
                        <HardwareProfileForm
                          onSubmit={handleHardwareSave}
                          initialValues={hardwareProfile || {}}
                          isLoading={saving}
                        />
                      </div>
                    )}
                  </div>

                  {/* ── Skill Level ── */}
                  <div className="glass-card padding--lg" style={{
                    background: 'rgba(15,23,42,0.5)', backdropFilter: 'blur(12px)',
                    border: '1px solid rgba(0,243,255,0.2)', borderRadius: '12px',
                  }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
                      <h2 style={{ color: '#00F3FF', margin: 0 }}>Skill Level</h2>
                      <button
                        onClick={() => { setEditingSkill(!editingSkill); setEditingHardware(false); setLocalSkill(skillLevel); }}
                        style={{
                          padding: '0.4rem 1rem', background: 'rgba(0,243,255,0.1)',
                          border: '1px solid #00F3FF', borderRadius: '8px',
                          color: '#00F3FF', cursor: 'pointer', fontSize: '0.875rem',
                        }}
                      >
                        {editingSkill ? '✕ Cancel' : '✏️ Edit Skill'}
                      </button>
                    </div>

                    {!editingSkill && (
                      <div style={{
                        display: 'inline-flex', alignItems: 'center', gap: '0.75rem',
                        padding: '0.75rem 1.5rem',
                        background: 'rgba(0,243,255,0.08)', border: '1px solid rgba(0,243,255,0.3)',
                        borderRadius: '12px',
                      }}>
                        <span style={{ fontSize: '1.5rem' }}>
                          {skillLevel === 'beginner' ? '🌱' : skillLevel === 'intermediate' ? '🚀' : '⚡'}
                        </span>
                        <span style={{ color: '#fff', fontWeight: 600, textTransform: 'capitalize' }}>
                          {skillLevel}
                        </span>
                      </div>
                    )}

                    {editingSkill && (
                      <form onSubmit={handleSkillSave} style={{ marginTop: '0.5rem' }}>
                        <SkillLevelSelector
                          value={localSkill}
                          onChange={setLocalSkill}
                          showDescriptions
                          direction="vertical"
                        />
                        <button
                          type="submit"
                          disabled={saving}
                          style={{
                            marginTop: '1.5rem', width: '100%', padding: '0.875rem',
                            background: 'rgba(0,243,255,0.1)', border: '2px solid #00F3FF',
                            color: '#00F3FF', borderRadius: '8px', fontWeight: 600,
                            cursor: saving ? 'not-allowed' : 'pointer', opacity: saving ? 0.6 : 1,
                          }}
                        >
                          {saving ? 'Saving...' : 'Save Skill Level'}
                        </button>
                      </form>
                    )}
                  </div>
                </>
              )}

            </div>
          </div>
        </main>
      </Layout>
    </AuthGuard>
  );
}
