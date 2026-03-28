/**
 * Authentication hook for managing auth state.
 * 
 * Provides user, loading state, and auth functions.
 */

import React, { useState, useEffect, createContext, useContext } from 'react';

// Use environment variable for API URL with fallback
// Webpack 5 does not polyfill process. Docusaurus injects env vars only at compile-time.
// For runtime config, use docusaurus.config.ts customFields + useDocusaurusContext().
const API_BASE_URL = 'http://localhost:8000';

// TypeScript interfaces
interface User {
  id: string;
  email: string;
  email_verified: boolean;
  is_admin?: boolean;
}

interface AuthProviderProps {
  children: React.ReactNode;
}

interface AuthState {
  user: User | null;
  loading: boolean;
  error: string | null;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  loginWithGithub: () => void;
}

// Auth Context
const AuthContext = createContext<AuthState | null>(null);

/**
 * Auth Provider component
 */
export function AuthProvider({ children }: AuthProviderProps) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Check for existing session on mount
  useEffect(() => {
    checkAuth();
  }, []);

  /**
   * Check if user is authenticated
   */
  async function checkAuth() {
    try {
      const token = localStorage.getItem('access_token');
      if (!token) {
        setLoading(false);
        return;
      }

      const response = await fetch(`${API_BASE_URL}/api/auth/me`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (response.ok) {
        const userData = await response.json();
        setUser(userData);
        
        // Store admin status for navbar
        if (userData.is_admin) {
          localStorage.setItem('is_admin', 'true');
        } else {
          localStorage.removeItem('is_admin');
        }
      } else {
        localStorage.removeItem('access_token');
      }
    } catch (err) {
      console.error('Auth check failed:', err);
    } finally {
      setLoading(false);
    }
  }

  /**
   * Login with email and password
   */
  async function login(email: string, password: string) {
    try {
      setError(null);
      const response = await fetch(`${API_BASE_URL}/api/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail?.message || 'Login failed');
      }

      const data = await response.json();
      localStorage.setItem('access_token', data.access_token);
      setUser(data.user);
      
      // Store admin status for navbar
      if (data.user && data.user.is_admin) {
        localStorage.setItem('is_admin', 'true');
      } else {
        localStorage.removeItem('is_admin');
      }
    } catch (err: any) {
      setError(err.message);
      throw err;
    }
  }

  /**
   * Register with email and password
   */
  async function register(email: string, password: string) {
    try {
      setError(null);
      const response = await fetch(`${API_BASE_URL}/api/auth/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail?.message || 'Registration failed');
      }

      const data = await response.json();
      localStorage.setItem('access_token', data.access_token);
      setUser(data.user);
    } catch (err: any) {
      setError(err.message);
      throw err;
    }
  }

  /**
   * Logout user
   */
  async function logout() {
    try {
      const token = localStorage.getItem('access_token');
      if (token) {
        await fetch(`${API_BASE_URL}/api/auth/logout`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`,
          },
        });
      }
    } catch (err) {
      console.error('Logout failed:', err);
    } finally {
      localStorage.removeItem('access_token');
      localStorage.removeItem('is_admin');
      setUser(null);
    }
  }

  /**
   * Login with GitHub OAuth
   */
  function loginWithGithub() {
    window.location.href = `${API_BASE_URL}/api/auth/github`;
  }

  const value: AuthState = {
    user,
    loading,
    error,
    login,
    register,
    logout,
    loginWithGithub,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

/**
 * Use auth hook
 */
export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
