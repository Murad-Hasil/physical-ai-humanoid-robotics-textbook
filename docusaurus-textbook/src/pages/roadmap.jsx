/**
 * Roadmap Page
 *
 * Visual 13-week learning path with completion tracking.
 * Features glassmorphic design with neon accents.
 */

import React from 'react';
import Layout from '@theme/Layout';
import { useAuth } from '@site/src/hooks/useAuth';
import AuthGuard from '@site/src/components/AuthGuard';
import Roadmap from '@site/src/components/Roadmap';

export default function RoadmapPage() {
  const { user } = useAuth();

  return (
    <AuthGuard>
      <Layout
        title="Curriculum Roadmap"
        description="Track your progress through the 13-week Physical AI curriculum"
      >
        <main className="container margin-vert--lg">
          <div className="row">
            <div className="col col--10 col--offset-1">
              <div className="glass-card padding--lg margin-bottom--lg" style={{
                background: 'rgba(15, 23, 42, 0.5)',
                backdropFilter: 'blur(12px)',
                border: '1px solid rgba(59, 130, 246, 0.2)',
                boxShadow: '0 8px 32px 0 rgba(0, 255, 255, 0.1)',
              }}>
                <div className="text--center margin-bottom--lg">
                  <h1 className="neon-text" style={{ fontSize: '2.5rem' }}>
                    13-Week Curriculum Roadmap
                  </h1>
                  <p className="text--muted" style={{ 
                    marginTop: '0.5rem',
                    fontSize: '1.1rem',
                  }}>
                    Track your progress through the Physical AI program
                  </p>
                </div>

                {/* User Info Badge */}
                {user && (
                  <div className="margin-bottom--lg" style={{
                    display: 'inline-flex',
                    alignItems: 'center',
                    padding: '0.5rem 1rem',
                    background: 'rgba(0, 255, 255, 0.1)',
                    border: '1px solid rgba(0, 255, 255, 0.3)',
                    borderRadius: '20px',
                    fontSize: '0.9rem',
                  }}>
                    <span style={{
                      width: '8px',
                      height: '8px',
                      borderRadius: '50%',
                      background: '#00FFFF',
                      marginRight: '0.5rem',
                      boxShadow: '0 0 10px rgba(0, 255, 255, 0.5)',
                    }}></span>
                    <strong style={{ marginLeft: '0.5rem', color: '#00FFFF' }}>{user.email}</strong>
                  </div>
                )}

                <Roadmap />
              </div>
            </div>
          </div>
        </main>
      </Layout>
    </AuthGuard>
  );
}
