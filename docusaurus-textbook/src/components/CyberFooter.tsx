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
            <div style={{ display: 'flex', gap: '1rem', marginBottom: '1.5rem', flexWrap: 'wrap' }}>
              <a
                href="https://github.com/Murad-Hasil/physical-ai-humanoid-robotics-textbook"
                target="_blank"
                rel="noopener noreferrer"
                title="GitHub Repository"
                style={{ color: '#00F3FF', fontSize: '1.5rem', textDecoration: 'none' }}
              >🐙</a>
              <a
                href="https://www.linkedin.com/in/muradhasil/"
                target="_blank"
                rel="noopener noreferrer"
                title="LinkedIn"
                style={{ color: '#00F3FF', fontSize: '1.5rem', textDecoration: 'none' }}
              >💼</a>
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
