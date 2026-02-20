import React from 'react';
import StatusIndicator from './StatusIndicator';

export default function Header({ online }) {
  return (
    <header className="header">
      <div className="header-title">
        <h1>InfoFlow AI</h1>
        <span className="header-subtitle">Enterprise Knowledge Assistant</span>
      </div>
      <StatusIndicator online={online} />
    </header>
  );
}
