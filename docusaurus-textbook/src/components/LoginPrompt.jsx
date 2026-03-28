/**
 * Login Prompt Component
 *
 * Displays login call-to-action for unauthenticated users.
 */

import React from 'react';

export default function LoginPrompt() {
  return (
    <div className="container margin-vert--xl">
      <div className="row">
        <div className="col col--6 col--offset-3">
          <div className="glass-card padding--xl text--center" style={{
            background: 'rgba(15, 23, 42, 0.5)',
            backdropFilter: 'blur(12px)',
            border: '1px solid rgba(59, 130, 246, 0.2)',
          }}>
            <h1 className="neon-text margin-bottom--lg" style={{ fontSize: '2rem' }}>
              Login Required
            </h1>
            <p className="text--muted margin-bottom--xl">
              Please log in to access this page and unlock all features including:
            </p>

            <div className="glass-panel margin-bottom--lg" style={{ textAlign: 'left' }}>
              <ul style={{ lineHeight: '2' }}>
                <li>✓ Configure your hardware setup (RTX, Jetson, Unitree)</li>
                <li>✓ Track 13-week curriculum progress</li>
                <li>✓ Get personalized AI assistance</li>
                <li>✓ Save chat history and continue conversations</li>
              </ul>
            </div>

            <div className="margin-top--xl">
              <a
                href="/login"
                className="button button--primary button--lg margin-right--md"
                style={{
                  background: 'rgba(0, 255, 255, 0.1)',
                  border: '2px solid #00FFFF',
                  color: '#00FFFF',
                  boxShadow: '0 0 10px rgba(0, 255, 255, 0.3)',
                }}
              >
                Sign In
              </a>
              <a
                href="/signup"
                className="button button--outline button--lg"
                style={{
                  border: '2px solid #00FFFF',
                  color: '#00FFFF',
                }}
              >
                Create Account
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
