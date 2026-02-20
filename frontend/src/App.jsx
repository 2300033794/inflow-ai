import React, { useState, useEffect, useCallback } from 'react';
import Header from './components/Header';
import ChatWindow from './components/ChatWindow';
import ChatInput from './components/ChatInput';
import { sendChat, checkHealth } from './api/api';

const HEALTH_POLL_INTERVAL_MS = 15000;
let nextMsgId = 0;

export default function App() {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [online, setOnline] = useState(false);

  useEffect(() => {
    const poll = () => {
      checkHealth()
        .then(() => setOnline(true))
        .catch(() => setOnline(false));
    };
    poll();
    const id = setInterval(poll, HEALTH_POLL_INTERVAL_MS);
    return () => clearInterval(id);
  }, []);

  const handleSend = useCallback(async (query) => {
    setMessages((prev) => [...prev, { id: ++nextMsgId, role: 'user', text: query }]);
    setLoading(true);
    try {
      const data = await sendChat(query);
      setMessages((prev) => [
        ...prev,
        { id: ++nextMsgId, role: 'ai', text: data.answer, sources: data.sources },
      ]);
    } catch {
      setMessages((prev) => [
        ...prev,
        { id: ++nextMsgId, role: 'ai', text: 'Sorry, something went wrong. Please try again.' },
      ]);
    } finally {
      setLoading(false);
    }
  }, []);

  return (
    <div className="app">
      <Header online={online} />
      <main className="chat-container">
        <ChatWindow messages={messages} loading={loading} />
        <ChatInput onSend={handleSend} disabled={loading} />
      </main>
    </div>
  );
}
