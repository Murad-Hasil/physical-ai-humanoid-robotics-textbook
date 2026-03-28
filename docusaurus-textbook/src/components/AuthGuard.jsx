/**
 * Auth Guard Component
 * 
 * Protects routes by redirecting unauthenticated users to login prompt.
 */

import React from 'react';
import { useAuth } from '@site/src/hooks/useAuth';
import LoginPrompt from './LoginPrompt';

export default function AuthGuard({ children }) {
  const { user, loading } = useAuth();

  // Show loading state while checking authentication
  if (loading) {
    return (
      <div className="container margin-vert--xl text--center">
        <div className="spinner spinner--lg"></div>
        <p className="margin-top--md">Loading...</p>
      </div>
    );
  }

  // Redirect to login prompt if not authenticated
  if (!user) {
    return <LoginPrompt />;
  }

  // User is authenticated - render protected content
  return children;
}
