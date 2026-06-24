import React, { useState, useRef, useEffect } from 'react';
import { Send, Sun, Moon, Database, MessageSquare, Trash2, BookOpen } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';
import './ChatInterface.css';

const ChatInterface = ({ theme, toggleTheme, onShowData, onShowKnowledge, messages, setMessages, sessionId, onClearChat }) => {
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = { role: 'user', content: input, timestamp: new Date() };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const response = await axios.post('http://localhost:8002/ask', {
        question: input,
        thread_id: sessionId
      });

      const assistantMessage = {
        role: 'assistant',
        content: response.data.answer,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      const errorMessage = {
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please make sure the backend server is running.',
        timestamp: new Date(),
        error: true
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const clearChat = () => {
    if (window.confirm('Are you sure you want to clear the chat history? This will start a new session.')) {
      onClearChat();
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="chat-container">
      <div className={`chat-header glass-${theme}`}>
        <div className="header-left">
          <img src="/fluid-ai.png" alt="Logo" className="logo-img" />
          <div className="header-text">
            <h1>Enterprise AI Assistant</h1>
            <div className="session-info">
              <span className="session-label">Session:</span>
              <span className="session-id">{sessionId}</span>
              <span className="message-count">({messages.length} messages)</span>
            </div>
          </div>
        </div>
        <div className="header-actions">
          <button onClick={clearChat} className="icon-btn" title="Clear Chat & Start New Session">
            <Trash2 size={20} />
          </button>
          <button onClick={onShowKnowledge} className="icon-btn" title="Knowledge Base">
            <BookOpen size={20} />
          </button>
          <button onClick={onShowData} className="icon-btn" title="View Database">
            <Database size={20} />
          </button>
          <button onClick={toggleTheme} className="icon-btn" title="Toggle Theme">
            {theme === 'dark' ? <Sun size={20} /> : <Moon size={20} />}
          </button>
        </div>
      </div>

      <div className="chat-messages">
        <AnimatePresence>
          {messages.map((msg, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0 }}
              className={`message ${msg.role} ${msg.error ? 'error' : ''}`}
            >
              <div className={`message-bubble glass-${theme}`}>
                <div className="message-content">
                  {msg.role === 'assistant' ? (
                    <ReactMarkdown>{msg.content}</ReactMarkdown>
                  ) : (
                    msg.content
                  )}
                </div>
                <div className="message-time">
                  {msg.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                </div>
              </div>
            </motion.div>
          ))}
        </AnimatePresence>
        
        {loading && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="message assistant"
          >
            <div className={`message-bubble glass-${theme}`}>
              <div className="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </motion.div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className={`chat-input-container glass-${theme}`}>
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Ask me anything about employees, tickets, or reports..."
          rows="1"
          disabled={loading}
        />
        <button
          onClick={sendMessage}
          disabled={!input.trim() || loading}
          className="send-btn"
        >
          <Send size={20} />
        </button>
      </div>
    </div>
  );
};

export default ChatInterface;
