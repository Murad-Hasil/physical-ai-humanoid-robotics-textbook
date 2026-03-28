/**
 * Roadmap Component
 *
 * Visual 13-week learning path with completion tracking.
 * Progress is stored in localStorage (backend endpoint not yet available).
 */

import React, { useState, useEffect } from 'react';

const WEEKS_DATA = [
  { week: 1,  title: 'Introduction to Physical AI',     module: '01-foundation' },
  { week: 2,  title: 'Physical AI Architecture',         module: '01-foundation' },
  { week: 3,  title: 'Introduction to ROS 2',            module: '02-ros-2' },
  { week: 4,  title: 'ROS 2 Nodes and Topics',           module: '02-ros-2' },
  { week: 5,  title: 'ROS 2 Services and Actions',       module: '02-ros-2' },
  { week: 6,  title: 'Introduction to Gazebo',           module: '03-gazebo' },
  { week: 7,  title: 'Robot Modeling in Gazebo',         module: '03-gazebo' },
  { week: 8,  title: 'Introduction to NVIDIA Isaac Sim', module: '04-nvidia-isaac' },
  { week: 9,  title: 'ISAAC ROS Integration',            module: '04-nvidia-isaac' },
  { week: 10, title: 'Humanoid Locomotion',              module: '05-humanoid' },
  { week: 11, title: 'Conversational AI Integration',    module: '05-humanoid' },
  { week: 12, title: 'Complete Humanoid System',         module: '05-humanoid' },
  { week: 13, title: 'Capstone Project',                 module: '05-humanoid' },
];

const STORAGE_KEY = 'roadmap_progress';

function loadProgress() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    return raw ? JSON.parse(raw) : [];
  } catch {
    return [];
  }
}

function saveProgress(completed) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(completed));
}

export default function Roadmap() {
  const [completedWeeks, setCompletedWeeks] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setCompletedWeeks(loadProgress());
    setLoading(false);
  }, []);

  function isCompleted(week) {
    return completedWeeks.includes(week);
  }

  function toggleWeek(week) {
    setCompletedWeeks(prev => {
      const updated = prev.includes(week)
        ? prev.filter(w => w !== week)
        : [...prev, week];
      saveProgress(updated);
      return updated;
    });
  }

  if (loading) {
    return (
      <div style={{ textAlign: 'center', padding: '2rem', color: '#aaa' }}>
        Loading your progress...
      </div>
    );
  }

  const completedCount = completedWeeks.length;
  const pct = Math.round((completedCount / 13) * 100);

  return (
    <div>
      <h2 style={{ textAlign: 'center', color: '#00F3FF', marginBottom: '0.5rem' }}>
        Your Learning Path
      </h2>
      <p style={{ textAlign: 'center', color: '#888', marginBottom: '2rem' }}>
        Click a week to mark it complete. Progress is saved locally.
      </p>

      {/* Timeline */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
        {WEEKS_DATA.map((w) => {
          const done = isCompleted(w.week);
          return (
            <div
              key={w.week}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '1rem',
                padding: '1rem 1.25rem',
                background: done ? 'rgba(0,243,255,0.08)' : 'rgba(255,255,255,0.03)',
                border: `1px solid ${done ? 'rgba(0,243,255,0.4)' : 'rgba(255,255,255,0.1)'}`,
                borderRadius: '10px',
                transition: 'all 0.2s ease',
              }}
            >
              {/* Week Number Dot */}
              <div style={{
                width: '2.5rem',
                height: '2.5rem',
                borderRadius: '50%',
                background: done ? '#00F3FF' : 'rgba(0,243,255,0.1)',
                border: `2px solid ${done ? '#00F3FF' : 'rgba(0,243,255,0.3)'}`,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                flexShrink: 0,
                color: done ? '#000' : '#00F3FF',
                fontWeight: 'bold',
                fontSize: '0.9rem',
                boxShadow: done ? '0 0 12px rgba(0,243,255,0.5)' : 'none',
              }}>
                {done ? '✓' : w.week}
              </div>

              {/* Content */}
              <div style={{ flex: 1 }}>
                <div style={{ fontWeight: 600, color: done ? '#00F3FF' : '#e2e8f0', marginBottom: '2px' }}>
                  Week {w.week}: {w.title}
                </div>
                <div style={{ fontSize: '0.78rem', color: '#64748b' }}>
                  {w.module}
                </div>
              </div>

              {/* Toggle Button */}
              <button
                onClick={() => toggleWeek(w.week)}
                style={{
                  padding: '0.35rem 0.9rem',
                  borderRadius: '6px',
                  fontSize: '0.8rem',
                  fontWeight: 600,
                  cursor: 'pointer',
                  border: `1px solid ${done ? 'rgba(0,243,255,0.4)' : 'rgba(0,243,255,0.3)'}`,
                  background: done ? 'rgba(0,243,255,0.15)' : 'transparent',
                  color: done ? '#00F3FF' : '#94a3b8',
                  transition: 'all 0.2s ease',
                  flexShrink: 0,
                }}
              >
                {done ? '✓ Done' : 'Mark Done'}
              </button>
            </div>
          );
        })}
      </div>

      {/* Progress Summary */}
      <div style={{
        marginTop: '2rem',
        padding: '1.5rem',
        background: 'rgba(15,23,42,0.5)',
        border: '1px solid rgba(0,243,255,0.2)',
        borderRadius: '12px',
        textAlign: 'center',
      }}>
        <h3 style={{ color: '#00F3FF', marginBottom: '1rem' }}>Overall Progress</h3>

        {/* Progress Bar */}
        <div style={{
          height: '8px',
          background: 'rgba(255,255,255,0.1)',
          borderRadius: '4px',
          overflow: 'hidden',
          marginBottom: '0.75rem',
        }}>
          <div style={{
            width: `${pct}%`,
            height: '100%',
            background: 'linear-gradient(90deg, #00F3FF, #0080ff)',
            borderRadius: '4px',
            boxShadow: '0 0 8px rgba(0,243,255,0.5)',
            transition: 'width 0.4s ease',
          }} />
        </div>

        <p style={{ color: '#94a3b8', margin: 0 }}>
          <strong style={{ color: '#00F3FF' }}>{completedCount}</strong> of{' '}
          <strong style={{ color: '#00F3FF' }}>13</strong> weeks completed —{' '}
          <strong style={{ color: '#00F3FF' }}>{pct}%</strong>
        </p>
      </div>
    </div>
  );
}
