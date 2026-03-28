/**
 * Custom Cyber Footer Component
 */

import React from 'react';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';

export default function CyberFooter() {
  const {siteConfig} = useDocusaurusContext();
  const currentYear = new Date().getFullYear();

  return (
    <footer style={{
      background: 'linear-gradient(135deg, #111111 0%, #1A1A2E 100%)',
      borderTop: '2px solid #00F3FF',
      padding: '3rem 0 2rem',
      marginTop: '4rem'
    }}>
      <div className="container">
        {/* 4-Column Layout */}
        <div className="row">
          {/* Column 1: Brand */}
          <div className="col col--3">
            <h3 style={{ 
              color: '#00F3FF',
              fontSize: '1.5rem',
              marginBottom: '1rem',
              textShadow: '0 0 10px rgba(0, 243, 255, 0.5)'
            }}>
              🤖 Physical AI
            </h3>
            <p style={{ color: '#A0A0B0', lineHeight: '1.6' }}>
              Master the future of robotics with our comprehensive curriculum covering Edge AI, RAG, and Sim-to-Real deployment.
            </p>
          </div>

          {/* Column 2: Quick Links */}
          <div className="col col--3">
            <h4 style={{ color: '#00F3FF', marginBottom: '1rem', fontSize: '1.1rem' }}>
              Quick Links
            </h4>
            <ul style={{ listStyle: 'none', padding: 0, margin: 0 }}>
              <li style={{ marginBottom: '0.75rem' }}>
                <a href="/physical-ai-humanoid-robotics-textbook/docs/introduction-to-physical-ai" style={{ color: '#E0E0E0', textDecoration: 'none' }}>📚 Documentation</a>
              </li>
              <li style={{ marginBottom: '0.75rem' }}>
                <a href="/physical-ai-humanoid-robotics-textbook/roadmap" style={{ color: '#E0E0E0', textDecoration: 'none' }}>🗺️ 13-Week Roadmap</a>
              </li>
              <li style={{ marginBottom: '0.75rem' }}>
                <a href="/physical-ai-humanoid-robotics-textbook/profile" style={{ color: '#E0E0E0', textDecoration: 'none' }}>🖥️ Dashboard</a>
              </li>
              <li style={{ marginBottom: '0.75rem' }}>
                <a href="/physical-ai-humanoid-robotics-textbook/admin/ingest" style={{ color: '#E0E0E0', textDecoration: 'none' }}>🛡️ Admin</a>
              </li>
            </ul>
          </div>

          {/* Column 3: System Status */}
          <div className="col col--3">
            <h4 style={{ color: '#00F3FF', marginBottom: '1rem', fontSize: '1.1rem' }}>
              System Status
            </h4>
            <div className="glass-panel" style={{ padding: '1rem', marginBottom: '0.75rem', border: '1px solid rgba(0, 243, 255, 0.2)' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <div style={{ width: '10px', height: '10px', borderRadius: '50%', background: '#00FF00', boxShadow: '0 0 10px rgba(0, 255, 0, 0.5)' }} />
                <span style={{ color: '#E0E0E0', fontSize: '0.9rem' }}>PostgreSQL</span>
              </div>
            </div>
            <div className="glass-panel" style={{ padding: '1rem', marginBottom: '0.75rem', border: '1px solid rgba(0, 243, 255, 0.2)' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <div style={{ width: '10px', height: '10px', borderRadius: '50%', background: '#00FF00', boxShadow: '0 0 10px rgba(0, 255, 0, 0.5)' }} />
                <span style={{ color: '#E0E0E0', fontSize: '0.9rem' }}>Qdrant Cloud</span>
              </div>
            </div>
            <div className="glass-panel" style={{ padding: '1rem', border: '1px solid rgba(0, 243, 255, 0.2)' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <div style={{ width: '10px', height: '10px', borderRadius: '50%', background: '#00FF00', boxShadow: '0 0 10px rgba(0, 255, 0, 0.5)' }} />
                <span style={{ color: '#E0E0E0', fontSize: '0.9rem' }}>Grok API</span>
              </div>
            </div>
          </div>

          {/* Column 4: Social & Legal */}
          <div className="col col--3">
            <h4 style={{ color: '#00F3FF', marginBottom: '1rem', fontSize: '1.1rem' }}>
              Connect
            </h4>
            <div style={{ display: 'flex', gap: '0.75rem', marginBottom: '1.5rem', flexWrap: 'wrap' }}>
              <a
                href="https://github.com/Murad-Hasil/physical-ai-humanoid-robotics-textbook"
                target="_blank"
                rel="noopener noreferrer"
                title="GitHub Repository"
                style={{
                  display: 'flex', alignItems: 'center', justifyContent: 'center',
                  width: '40px', height: '40px', borderRadius: '8px',
                  background: 'rgba(0, 243, 255, 0.08)',
                  border: '1px solid rgba(0, 243, 255, 0.25)',
                  color: '#00F3FF', textDecoration: 'none',
                  transition: 'all 0.2s ease',
                }}
                onMouseEnter={e => {
                  (e.currentTarget as HTMLAnchorElement).style.background = 'rgba(0, 243, 255, 0.18)';
                  (e.currentTarget as HTMLAnchorElement).style.borderColor = '#00F3FF';
                  (e.currentTarget as HTMLAnchorElement).style.boxShadow = '0 0 12px rgba(0,243,255,0.3)';
                }}
                onMouseLeave={e => {
                  (e.currentTarget as HTMLAnchorElement).style.background = 'rgba(0, 243, 255, 0.08)';
                  (e.currentTarget as HTMLAnchorElement).style.borderColor = 'rgba(0, 243, 255, 0.25)';
                  (e.currentTarget as HTMLAnchorElement).style.boxShadow = 'none';
                }}
              >
                {/* GitHub SVG */}
                <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
                  <path d="M12 0C5.37 0 0 5.37 0 12c0 5.3 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61-.546-1.385-1.335-1.755-1.335-1.755-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 21.795 24 17.295 24 12c0-6.63-5.37-12-12-12"/>
                </svg>
              </a>
              <a
                href="https://www.linkedin.com/in/muradhasil/"
                target="_blank"
                rel="noopener noreferrer"
                title="LinkedIn"
                style={{
                  display: 'flex', alignItems: 'center', justifyContent: 'center',
                  width: '40px', height: '40px', borderRadius: '8px',
                  background: 'rgba(0, 243, 255, 0.08)',
                  border: '1px solid rgba(0, 243, 255, 0.25)',
                  color: '#00F3FF', textDecoration: 'none',
                  transition: 'all 0.2s ease',
                }}
                onMouseEnter={e => {
                  (e.currentTarget as HTMLAnchorElement).style.background = 'rgba(0, 243, 255, 0.18)';
                  (e.currentTarget as HTMLAnchorElement).style.borderColor = '#00F3FF';
                  (e.currentTarget as HTMLAnchorElement).style.boxShadow = '0 0 12px rgba(0,243,255,0.3)';
                }}
                onMouseLeave={e => {
                  (e.currentTarget as HTMLAnchorElement).style.background = 'rgba(0, 243, 255, 0.08)';
                  (e.currentTarget as HTMLAnchorElement).style.borderColor = 'rgba(0, 243, 255, 0.25)';
                  (e.currentTarget as HTMLAnchorElement).style.boxShadow = 'none';
                }}
              >
                {/* LinkedIn SVG */}
                <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
                  <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 01-2.063-2.065 2.064 2.064 0 112.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
                </svg>
              </a>
            </div>
            
            {/* Watermark */}
            <div className="glass-panel" style={{ padding: '0.75rem', textAlign: 'center', border: '1px solid rgba(0, 243, 255, 0.2)', background: 'rgba(0, 243, 255, 0.05)' }}>
              <p style={{ margin: 0, fontSize: '0.85rem', color: '#00F3FF', textShadow: '0 0 5px rgba(0, 243, 255, 0.3)' }}>
                ⚡ Powered by GIAIC & Grok
              </p>
            </div>
          </div>
        </div>

        {/* Bottom Bar */}
        <div style={{ marginTop: '3rem', paddingTop: '2rem', borderTop: '1px solid rgba(0, 243, 255, 0.2)', textAlign: 'center' }}>
          <p style={{ color: '#A0A0B0', margin: 0 }}>
            © {currentYear} {siteConfig.title}. Built with 🤖 by GIAIC
          </p>
        </div>
      </div>
    </footer>
  );
}
