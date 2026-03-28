/**
 * Root component for Docusaurus app.
 *
 * Wraps the entire application with providers (Auth, Hardware).
 * Mounts the ChatWidget globally on every page.
 */

import React from 'react';
import { AuthProvider } from '../hooks/useAuth';
import { HardwareProvider } from '../context/HardwareContext';
import ChatWidget from '../components/ChatWidget';

export default function Root({ children }) {
  return (
    <AuthProvider>
      <HardwareProvider>
        {children}
        <ChatWidget />
      </HardwareProvider>
    </AuthProvider>
  );
}
