/**
 * System Status Component
 * 
 * Displays user's active hardware in chatbot widget header.
 */

import React from 'react';
import { useHardware } from '@site/src/context/HardwareContext';
import clsx from 'clsx';

export default function SystemStatus() {
  const { hardwareProfile, loading, getHardwareDisplayString } = useHardware();
  const displayString = getHardwareDisplayString();

  return (
    <div className={clsx(
      'system-status',
      !hardwareProfile ? 'system-status--not-configured' : 'system-status--active'
    )}>
      <div className="system-status__indicator"></div>
      <span className="system-status__label">
        {loading ? (
          <>
            <span className="spinner spinner--xs margin-right--xs"></span>
            Loading...
          </>
        ) : (
          <>
            Mode: {displayString}
            {!hardwareProfile && (
              <a href="/physical-ai-humanoid-robotics-textbook/profile" className="system-status__link margin-left--xs">
                (Configure)
              </a>
            )}
          </>
        )}
      </span>
    </div>
  );
}
