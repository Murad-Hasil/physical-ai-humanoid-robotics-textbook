/**
 * Login Button component for Docusaurus navbar.
 * 
 * Shows login/logout button based on auth state.
 */

import React, { useState } from 'react';
import { useAuth } from '../hooks/useAuth';

export function LoginButton() {
  const { user, loading, logout, login, register, loginWithGithub } = useAuth();
  const [showModal, setShowModal] = useState(false);
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleLogout = async () => {
    await logout();
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    
    try {
      if (isLogin) {
        await login(email, password);
      } else {
        await register(email, password);
      }
      setShowModal(false);
      setEmail('');
      setPassword('');
    } catch (err: any) {
      setError(err.message);
    }
  };

  const openLoginModal = () => {
    setIsLogin(true);
    setError('');
    setShowModal(true);
  };

  const openRegisterModal = () => {
    setIsLogin(false);
    setError('');
    setShowModal(true);
  };

  // Loading state
  if (loading) {
    return (
      <button className="button button--secondary" disabled>
        Loading...
      </button>
    );
  }

  // Logged in state
  if (user) {
    return (
      <>
        <button 
          className="button button--secondary"
          onClick={handleLogout}
        >
          Sign Out ({user.email})
        </button>
      </>
    );
  }

  // Logged out state
  return (
    <>
      <div style={{ display: 'flex', gap: '8px' }}>
        <button 
          className="button button--secondary"
          onClick={openLoginModal}
        >
          Sign In
        </button>
        <button 
          className="button button--primary"
          onClick={openRegisterModal}
        >
          Sign Up
        </button>
      </div>

      {showModal && (
        <div 
          style={{
            position: 'fixed',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            backgroundColor: 'rgba(0,0,0,0.5)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            zIndex: 1000,
          }}
          onClick={() => setShowModal(false)}
        >
          <div 
            style={{
              backgroundColor: 'white',
              padding: '24px',
              borderRadius: '8px',
              maxWidth: '400px',
              width: '90%',
              color: 'black',
            }}
            onClick={(e) => e.stopPropagation()}
          >
            <h2 style={{ marginTop: 0 }}>
              {isLogin ? 'Sign In' : 'Create Account'}
            </h2>
            
            <form onSubmit={handleSubmit}>
              <div style={{ marginBottom: '16px' }}>
                <label style={{ display: 'block', marginBottom: '4px' }}>
                  Email
                </label>
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                  style={{
                    width: '100%',
                    padding: '8px',
                    borderRadius: '4px',
                    border: '1px solid #ccc',
                  }}
                />
              </div>
              
              <div style={{ marginBottom: '16px' }}>
                <label style={{ display: 'block', marginBottom: '4px' }}>
                  Password
                </label>
                <input
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                  minLength={8}
                  style={{
                    width: '100%',
                    padding: '8px',
                    borderRadius: '4px',
                    border: '1px solid #ccc',
                  }}
                />
              </div>

              {error && (
                <div style={{ 
                  color: 'red', 
                  marginBottom: '16px',
                  fontSize: '14px',
                }}>
                  {error}
                </div>
              )}
              
              <button 
                type="submit" 
                className="button button--primary"
                style={{ width: '100%', marginBottom: '16px' }}
              >
                {isLogin ? 'Sign In' : 'Sign Up'}
              </button>
              
              <div style={{ textAlign: 'center', marginBottom: '16px' }}>
                <span style={{ color: '#666' }}>or</span>
              </div>
              
              <button 
                type="button"
                className="button button--secondary"
                onClick={loginWithGithub}
                style={{ width: '100%' }}
              >
                Sign in with GitHub
              </button>
              
              <div style={{ marginTop: '16px', textAlign: 'center' }}>
                <button
                  type="button"
                  onClick={() => {
                    setIsLogin(!isLogin);
                    setError('');
                  }}
                  style={{
                    background: 'none',
                    border: 'none',
                    color: '#007bff',
                    cursor: 'pointer',
                    textDecoration: 'underline',
                  }}
                >
                  {isLogin 
                    ? "Don't have an account? Sign Up" 
                    : "Already have an account? Sign In"}
                </button>
              </div>
              
              <button
                type="button"
                onClick={() => setShowModal(false)}
                style={{
                  marginTop: '16px',
                  background: 'none',
                  border: 'none',
                  color: '#666',
                  cursor: 'pointer',
                  width: '100%',
                }}
              >
                Cancel
              </button>
            </form>
          </div>
        </div>
      )}
    </>
  );
}
