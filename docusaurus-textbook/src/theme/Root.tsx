/**
 * Root wrapper for Auth + Hardware providers and global ChatWidget.
 *
 * Root.tsx takes precedence over Root.js in Docusaurus (TypeScript first).
 * Both AuthProvider and HardwareProvider must be here so every page has
 * access to auth state and hardware context.
 */

import React from 'react';
import { AuthProvider } from '@site/src/hooks/useAuth';
import { HardwareProvider } from '@site/src/context/HardwareContext';
import { PersonalizationProvider } from '@site/src/context/PersonalizationContext';
import ChatWidget from '@site/src/components/ChatWidget';

export default function Root({ children }) {
  return (
    <AuthProvider>
      <HardwareProvider>
        <PersonalizationProvider>
          {children}
          <ChatWidget />
        </PersonalizationProvider>
      </HardwareProvider>
    </AuthProvider>
  );
}
