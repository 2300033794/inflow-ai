import React from 'react';

export default function SourceList({ sources }) {
  if (!sources || sources.length === 0) return null;

  return (
    <div className="source-list">
      <span className="source-label">Sources:</span>
      <ul>
        {sources.map((src) => (
          <li key={src}>{src}</li>
        ))}
      </ul>
    </div>
  );
}
