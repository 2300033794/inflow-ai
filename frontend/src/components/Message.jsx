import React from 'react';
import SourceList from './SourceList';

export default function Message({ role, text, sources }) {
  const isUser = role === 'user';

  return (
    <div className={`message ${isUser ? 'message-user' : 'message-ai'}`}>
      <div className="message-bubble">
        <p className="message-text">{text}</p>
        {!isUser && <SourceList sources={sources} />}
      </div>
    </div>
  );
}
