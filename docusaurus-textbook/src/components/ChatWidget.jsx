/**
 * ChatWidget Component
 *
 * Global AI chatbot widget mounted on every page.
 * Features glassmorphic design with neon accents.
 */

import React, { useState, useRef, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import { useAuth } from '@site/src/hooks/useAuth';

export default function ChatWidget() {
  const { siteConfig } = useDocusaurusContext();
  const API_BASE_URL = siteConfig.customFields?.apiUrl || 'http://localhost:8000';

  const { user } = useAuth();
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: 'Hi! I\'m your Physical AI assistant. Ask me anything about ROS 2, Gazebo, NVIDIA Isaac, or humanoid robotics!\n\n💡 **Tip:** Select any text on the page and click "Ask AI" to ask about it!',
    },
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  // Selected text tooltip state
  const [selectionTooltip, setSelectionTooltip] = useState(null); // { x, y, text }

  // Listen for text selection anywhere on the page
  useEffect(() => {
    const handleMouseUp = (e) => {
      // Don't trigger inside the chat widget itself
      const chatEl = document.getElementById('chat-widget-root');
      if (chatEl && chatEl.contains(e.target)) return;

      setTimeout(() => {
        const selection = window.getSelection();
        const selectedText = selection?.toString().trim();
        if (selectedText && selectedText.length > 10) {
          const range = selection.getRangeAt(0);
          const rect = range.getBoundingClientRect();
          setSelectionTooltip({
            x: rect.left + rect.width / 2,
            y: rect.top - 48,   // fixed positioning — no scrollY needed
            text: selectedText,
          });
        } else {
          setSelectionTooltip(null);
        }
      }, 10);
    };

    const handleMouseDown = (e) => {
      const chatEl = document.getElementById('chat-widget-root');
      if (chatEl && chatEl.contains(e.target)) return;
      // Clear tooltip on new click unless clicking the tooltip button itself
      const tooltipEl = document.getElementById('selection-tooltip');
      if (tooltipEl && tooltipEl.contains(e.target)) return;
      setSelectionTooltip(null);
    };

    document.addEventListener('mouseup', handleMouseUp);
    document.addEventListener('mousedown', handleMouseDown);
    return () => {
      document.removeEventListener('mouseup', handleMouseUp);
      document.removeEventListener('mousedown', handleMouseDown);
    };
  }, []);

  const handleAskAboutSelection = () => {
    if (!selectionTooltip) return;
    const contextMsg = `I have a question about this text from the book:\n\n> "${selectionTooltip.text}"\n\nCan you explain this?`;
    setInput(contextMsg);
    setIsOpen(true);
    setSelectionTooltip(null);
    window.getSelection()?.removeAllRanges();
  };

  // Scroll to bottom when messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const toggleChat = () => setIsOpen(!isOpen);

  // Send message to backend
  const sendMessage = async (e) => {
    e.preventDefault();
    if (!input.trim() || loading) return;

    const userMessage = input.trim();
    setInput('');
    setLoading(true);

    setMessages(prev => [...prev, { role: 'user', content: userMessage }]);

    try {
      const token = localStorage.getItem('access_token');
      const headers = { 'Content-Type': 'application/json' };
      if (token) headers['Authorization'] = `Bearer ${token}`;

      const response = await fetch(`${API_BASE_URL}/api/chat`, {
        method: 'POST',
        headers,
        body: JSON.stringify({
          message: userMessage,
          conversation_id: 'default',
        }),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail?.message || `Server error: ${response.status}`);
      }

      const data = await response.json();
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: data.response || 'I received your message.',
        sources: data.sources || [],
        hardware_context_used: data.hardware_context_used || false,
      }]);
    } catch (err) {
      console.error('Chat error:', err);
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: `**Error:** ${err.message}`,
      }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div id="chat-widget-root">
      {/* Selected Text Tooltip */}
      {selectionTooltip && (
        <button
          id="selection-tooltip"
          onClick={handleAskAboutSelection}
          style={{
            position: 'fixed',
            left: `${selectionTooltip.x}px`,
            top: `${selectionTooltip.y}px`,
            transform: 'translateX(-50%)',
            zIndex: 99999,
            background: 'rgba(0, 255, 255, 0.15)',
            border: '1px solid rgba(0, 255, 255, 0.6)',
            borderRadius: '20px',
            color: '#00FFFF',
            fontSize: '0.78rem',
            fontWeight: '600',
            padding: '5px 14px',
            cursor: 'pointer',
            backdropFilter: 'blur(8px)',
            boxShadow: '0 0 16px rgba(0,255,255,0.3)',
            display: 'flex',
            alignItems: 'center',
            gap: '6px',
            whiteSpace: 'nowrap',
          }}
        >
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#00FFFF" strokeWidth="2.5">
            <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
          </svg>
          Ask AI about this
        </button>
      )}

      {/* Chat Toggle Button */}
      <button
        onClick={toggleChat}
        style={{
          position: 'fixed',
          bottom: '24px',
          right: '24px',
          width: '60px',
          height: '60px',
          borderRadius: '50%',
          background: 'rgba(0, 255, 255, 0.1)',
          border: '2px solid #00FFFF',
          boxShadow: '0 0 20px rgba(0, 255, 255, 0.4)',
          cursor: 'pointer',
          zIndex: 9999,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          transition: 'all 0.3s ease',
        }}
        onMouseEnter={(e) => {
          e.currentTarget.style.transform = 'scale(1.1)';
          e.currentTarget.style.boxShadow = '0 0 30px rgba(0, 255, 255, 0.6)';
        }}
        onMouseLeave={(e) => {
          e.currentTarget.style.transform = 'scale(1)';
          e.currentTarget.style.boxShadow = '0 0 20px rgba(0, 255, 255, 0.4)';
        }}
        aria-label="Toggle chat"
      >
        {isOpen ? (
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#00FFFF" strokeWidth="2">
            <path d="M18 6L6 18M6 6l12 12" />
          </svg>
        ) : (
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#00FFFF" strokeWidth="2">
            <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
          </svg>
        )}
      </button>

      {/* Chat Window */}
      {isOpen && (
        <div
          style={{
            position: 'fixed',
            bottom: '100px',
            right: '24px',
            width: '400px',
            maxWidth: 'calc(100vw - 48px)',
            height: '520px',
            maxHeight: 'calc(100vh - 120px)',
            background: 'rgba(15, 23, 42, 0.97)',
            backdropFilter: 'blur(16px)',
            border: '1px solid rgba(0, 255, 255, 0.3)',
            borderRadius: '16px',
            boxShadow: '0 8px 32px 0 rgba(0, 255, 255, 0.2), 0 0 40px rgba(0, 255, 255, 0.1)',
            zIndex: 9998,
            display: 'flex',
            flexDirection: 'column',
            overflow: 'hidden',
          }}
        >
          {/* Header */}
          <div
            style={{
              padding: '14px 18px',
              background: 'rgba(0, 255, 255, 0.08)',
              borderBottom: '1px solid rgba(0, 255, 255, 0.2)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <div
                style={{
                  width: '9px',
                  height: '9px',
                  borderRadius: '50%',
                  background: '#00FFFF',
                  boxShadow: '0 0 10px rgba(0, 255, 255, 0.7)',
                  animation: 'chatPulse 2s infinite',
                  flexShrink: 0,
                }}
              />
              <div>
                <h3 style={{ margin: 0, color: '#00FFFF', fontSize: '0.95rem', fontWeight: '600' }}>
                  Physical AI Assistant
                </h3>
                <p style={{ margin: 0, fontSize: '0.72rem', color: '#64748b' }}>
                  {user ? `${user.email}` : 'Guest mode · Login for personalized responses'}
                </p>
              </div>
            </div>
            <button
              onClick={toggleChat}
              style={{
                background: 'transparent',
                border: 'none',
                color: '#00FFFF',
                cursor: 'pointer',
                padding: '4px',
                display: 'flex',
                alignItems: 'center',
              }}
              aria-label="Close chat"
            >
              <svg width="18" height="18" viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M15 5L5 15M5 5l10 10" />
              </svg>
            </button>
          </div>

          {/* Messages */}
          <div
            className="chat-messages-scroll"
            style={{
              flex: 1,
              overflowY: 'auto',
              padding: '16px',
              display: 'flex',
              flexDirection: 'column',
              gap: '12px',
            }}
          >
            {messages.map((message, index) => (
              <div
                key={index}
                style={{
                  display: 'flex',
                  justifyContent: message.role === 'user' ? 'flex-end' : 'flex-start',
                }}
              >
                <div
                  style={{
                    maxWidth: '85%',
                    padding: '10px 14px',
                    borderRadius: '12px',
                    background: message.role === 'user'
                      ? 'rgba(0, 255, 255, 0.15)'
                      : 'rgba(255, 255, 255, 0.07)',
                    border: message.role === 'user'
                      ? '1px solid rgba(0, 255, 255, 0.3)'
                      : '1px solid rgba(255, 255, 255, 0.1)',
                    color: '#e2e8f0',
                    fontSize: '0.875rem',
                    lineHeight: '1.6',
                  }}
                >
                  {message.role === 'assistant' ? (
                    <div className="chat-markdown">
                      <ReactMarkdown remarkPlugins={[remarkGfm]}>
                        {message.content}
                      </ReactMarkdown>
                      {message.hardware_context_used && (
                        <span style={{
                          display: 'inline-block',
                          marginTop: '6px',
                          fontSize: '0.7rem',
                          color: '#00FFFF',
                          opacity: 0.7,
                        }}>
                          ⚡ Hardware-personalized
                        </span>
                      )}
                    </div>
                  ) : (
                    message.content
                  )}
                </div>
              </div>
            ))}
            {loading && (
              <div style={{ display: 'flex', justifyContent: 'flex-start' }}>
                <div
                  style={{
                    padding: '12px 16px',
                    borderRadius: '12px',
                    background: 'rgba(255, 255, 255, 0.07)',
                    border: '1px solid rgba(255, 255, 255, 0.1)',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '6px',
                  }}
                >
                  <div style={{
                    width: '8px', height: '8px', borderRadius: '50%',
                    background: '#00FFFF', animation: 'chatDot 1.2s infinite',
                  }} />
                  <div style={{
                    width: '8px', height: '8px', borderRadius: '50%',
                    background: '#00FFFF', animation: 'chatDot 1.2s 0.2s infinite',
                  }} />
                  <div style={{
                    width: '8px', height: '8px', borderRadius: '50%',
                    background: '#00FFFF', animation: 'chatDot 1.2s 0.4s infinite',
                  }} />
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Input */}
          <form
            onSubmit={sendMessage}
            style={{
              padding: '14px 16px',
              background: 'rgba(0, 0, 0, 0.3)',
              borderTop: '1px solid rgba(0, 255, 255, 0.15)',
              display: 'flex',
              gap: '10px',
            }}
          >
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask about ROS 2, Isaac, robotics..."
              disabled={loading}
              style={{
                flex: 1,
                padding: '9px 13px',
                background: 'rgba(15, 23, 42, 0.8)',
                border: '1px solid rgba(0, 255, 255, 0.25)',
                borderRadius: '8px',
                color: '#e2e8f0',
                fontSize: '0.875rem',
                outline: 'none',
              }}
              onFocus={(e) => {
                e.target.style.borderColor = '#00FFFF';
                e.target.style.boxShadow = '0 0 8px rgba(0, 255, 255, 0.25)';
              }}
              onBlur={(e) => {
                e.target.style.borderColor = 'rgba(0, 255, 255, 0.25)';
                e.target.style.boxShadow = 'none';
              }}
            />
            <button
              type="submit"
              disabled={loading || !input.trim()}
              style={{
                padding: '9px 18px',
                background: !input.trim() || loading ? 'rgba(0, 255, 255, 0.05)' : 'rgba(0, 255, 255, 0.15)',
                border: '1px solid rgba(0, 255, 255, 0.4)',
                borderRadius: '8px',
                color: '#00FFFF',
                fontWeight: '600',
                fontSize: '0.875rem',
                cursor: !input.trim() || loading ? 'not-allowed' : 'pointer',
                opacity: !input.trim() || loading ? 0.4 : 1,
                transition: 'all 0.2s ease',
              }}
            >
              Send
            </button>
          </form>
        </div>
      )}

      {/* Styles */}
      <style>{`
        #selection-tooltip {
          animation: tooltipFadeIn 0.15s ease;
        }
        @keyframes tooltipFadeIn {
          from { opacity: 0; transform: translateX(-50%) translateY(4px); }
          to { opacity: 1; transform: translateX(-50%) translateY(0); }
        }`}
      </style>
      <style>{`
        @keyframes chatPulse {
          0%, 100% { opacity: 1; box-shadow: 0 0 10px rgba(0, 255, 255, 0.7); }
          50% { opacity: 0.5; box-shadow: 0 0 4px rgba(0, 255, 255, 0.3); }
        }
        @keyframes chatDot {
          0%, 80%, 100% { transform: scale(0.6); opacity: 0.4; }
          40% { transform: scale(1); opacity: 1; }
        }
        .chat-messages-scroll::-webkit-scrollbar { width: 5px; }
        .chat-messages-scroll::-webkit-scrollbar-track { background: rgba(0,0,0,0.1); }
        .chat-messages-scroll::-webkit-scrollbar-thumb { background: rgba(0,255,255,0.25); border-radius: 3px; }

        /* Markdown styles inside chat */
        .chat-markdown p { margin: 0 0 6px 0; }
        .chat-markdown p:last-child { margin-bottom: 0; }
        .chat-markdown code {
          background: rgba(0, 255, 255, 0.1);
          border: 1px solid rgba(0, 255, 255, 0.2);
          padding: 1px 5px;
          border-radius: 4px;
          font-family: 'Courier New', monospace;
          font-size: 0.82em;
          color: #00FFFF;
        }
        .chat-markdown pre {
          background: rgba(0, 0, 0, 0.4);
          border: 1px solid rgba(0, 255, 255, 0.2);
          border-radius: 8px;
          padding: 10px 12px;
          overflow-x: auto;
          margin: 6px 0;
        }
        .chat-markdown pre code {
          background: transparent;
          border: none;
          padding: 0;
          color: #e2e8f0;
          font-size: 0.83em;
        }
        .chat-markdown ul, .chat-markdown ol { padding-left: 18px; margin: 4px 0; }
        .chat-markdown li { margin: 2px 0; }
        .chat-markdown strong { color: #fff; }
        .chat-markdown a { color: #00FFFF; }
        .chat-markdown h1, .chat-markdown h2, .chat-markdown h3 {
          color: #00FFFF; margin: 6px 0 4px 0; font-size: 1em;
        }
      `}</style>
    </div>
  );
}
