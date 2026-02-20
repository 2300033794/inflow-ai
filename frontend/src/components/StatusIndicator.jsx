import React from 'react';

export default function StatusIndicator({ online }) {
  return (
    <div className={`status-indicator ${online ? 'online' : 'offline'}`}>
      <span className="status-dot" />
      {online ? 'System Online' : 'System Offline'}
    </div>
  );
}
