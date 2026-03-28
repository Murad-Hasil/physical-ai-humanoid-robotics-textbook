/**
 * Login Page
 *
 * Glassmorphic login form connected to Better-Auth backend.
 */

import React, { useState } from 'react';
import Layout from '@theme/Layout';
import { useAuth } from '@site/src/hooks/useAuth';

export default function Login() {
  const { login, error: authError } = useAuth();
  const [formData, setFormData] = useState({
    email: '',
    password: '',
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value,
    }));
    setError('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      await login(formData.email, formData.password);
      // Redirect to profile page
      window.location.href = '/profile';
    } catch (err) {
      setError(err.message || 'Login failed. Please check your credentials.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Layout
      title="Login"
      description="Sign in to access your personalized hardware profile and curriculum"
    >
      <main className="container margin-vert--xl">
        <div className="row">
          <div className="col col--6 col--offset-3">
            <div className="glass-card padding--xl" style={{
              background: 'rgba(15, 23, 42, 0.5)',
              backdropFilter: 'blur(12px)',
              border: '1px solid rgba(59, 130, 246, 0.2)',
            }}>
              <div className="text--center margin-bottom--xl">
                <h1 className="neon-text" style={{ fontSize: '2.5rem' }}>
                  Welcome Back
                </h1>
                <p className="text--muted" style={{ marginTop: '0.5rem' }}>
                  Sign in to access your hardware dashboard and curriculum roadmap
                </p>
              </div>

              <form onSubmit={handleSubmit}>
                {/* Email Field */}
                <div className="margin-bottom--lg">
                  <label htmlFor="email" className="form-label" style={{
                    display: 'block',
                    marginBottom: '0.5rem',
                    color: '#00FFFF',
                    fontWeight: '600',
                  }}>
                    Email Address
                  </label>
                  <input
                    type="email"
                    id="email"
                    name="email"
                    value={formData.email}
                    onChange={handleChange}
                    className="glass-input"
                    style={{
                      width: '100%',
                      padding: '0.75rem 1rem',
                      background: 'rgba(15, 23, 42, 0.6)',
                      border: '1px solid rgba(59, 130, 246, 0.3)',
                      borderRadius: '0.5rem',
                      color: '#fff',
                      fontSize: '1rem',
                    }}
                    placeholder="you@example.com"
                    required
                  />
                </div>

                {/* Password Field */}
                <div className="margin-bottom--lg">
                  <label htmlFor="password" className="form-label" style={{
                    display: 'block',
                    marginBottom: '0.5rem',
                    color: '#00FFFF',
                    fontWeight: '600',
                  }}>
                    Password
                  </label>
                  <input
                    type="password"
                    id="password"
                    name="password"
                    value={formData.password}
                    onChange={handleChange}
                    className="glass-input"
                    style={{
                      width: '100%',
                      padding: '0.75rem 1rem',
                      background: 'rgba(15, 23, 42, 0.6)',
                      border: '1px solid rgba(59, 130, 246, 0.3)',
                      borderRadius: '0.5rem',
                      color: '#fff',
                      fontSize: '1rem',
                    }}
                    placeholder="••••••••"
                    required
                  />
                </div>

                {/* Error Message */}
                {(error || authError) && (
                  <div className="alert alert--danger margin-bottom--lg" role="alert">
                    {error || authError}
                  </div>
                )}

                {/* Submit Button */}
                <button
                  type="submit"
                  className="button button--primary button--block margin-bottom--md"
                  style={{
                    background: 'rgba(0, 255, 255, 0.1)',
                    border: '2px solid #00FFFF',
                    color: '#00FFFF',
                    padding: '0.875rem',
                    fontSize: '1rem',
                    fontWeight: '600',
                    textTransform: 'uppercase',
                    letterSpacing: '0.05em',
                    boxShadow: '0 0 10px rgba(0, 255, 255, 0.3)',
                    transition: 'all 0.3s ease',
                  }}
                  disabled={loading}
                  onMouseEnter={(e) => {
                    e.target.style.background = '#00FFFF';
                    e.target.style.color = '#000';
                    e.target.style.boxShadow = '0 0 20px rgba(0, 255, 255, 0.6)';
                  }}
                  onMouseLeave={(e) => {
                    e.target.style.background = 'rgba(0, 255, 255, 0.1)';
                    e.target.style.color = '#00FFFF';
                    e.target.style.boxShadow = '0 0 10px rgba(0, 255, 255, 0.3)';
                  }}
                >
                  {loading ? (
                    <>
                      <span className="spinner spinner--sm margin-right--sm"></span>
                      Signing In...
                    </>
                  ) : (
                    'Sign In'
                  )}
                </button>

                {/* Sign Up Link */}
                <div className="text--center margin-top--lg">
                  <p className="text--muted">
                    Don't have an account?{' '}
                    <a href="/signup" className="neon-link">
                      Create one
                    </a>
                  </p>
                </div>
              </form>
            </div>
          </div>
        </div>
      </main>
    </Layout>
  );
}
