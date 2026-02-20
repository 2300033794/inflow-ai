import React from 'react';

export default function SourceList({ sources }) {
  if (!sources || sources.length === 0) return null;

  return (
    <div className="source-list">
      <span className="source-label">Sources:</span>
      <ul>
        {sources.map((src, idx) => (
          <li key={idx}>{src}</li>
        ))}
      </ul>
    </div>
  );
}
