import React, { useEffect, useRef } from 'react';
import Message from './Message';

export default function ChatWindow({ messages, loading }) {
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  return (
    <div className="chat-window">
      {messages.length === 0 && (
        <div className="chat-empty">
          <p>Welcome to InfoFlow AI. Ask a question about company policies, IT support, or any internal knowledge.</p>
        </div>
      )}
      {messages.map((msg) => (
        <Message key={msg.id} role={msg.role} text={msg.text} sources={msg.sources} />
      ))}
      {loading && (
        <div className="message message-ai">
          <div className="message-bubble thinking">
            <span className="dot" /><span className="dot" /><span className="dot" />
            Thinking…
          </div>
        </div>
      )}
      <div ref={bottomRef} />
    </div>
  );
}
