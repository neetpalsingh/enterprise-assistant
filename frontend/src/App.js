import React, { useState } from 'react';
import ChatInterface from './components/ChatInterface';
import DataViewer from './components/DataViewer';
import KnowledgeBase from './components/KnowledgeBase';
import Loader from './components/Loader';
import './App.css';

function App() {
  const [theme, setTheme] = useState('dark');
  const [currentView, setCurrentView] = useState('chat');
  const [loading, setLoading] = useState(true);
  const [chatMessages, setChatMessages] = useState([]);
  const [sessionId, setSessionId] = useState(`session_${Date.now()}`);

  const toggleTheme = () => {
    setTheme(theme === 'dark' ? 'light' : 'dark');
  };

  const handleLoadComplete = () => {
    setLoading(false);
  };

  const handleClearChat = () => {
    setChatMessages([]);
    setSessionId(`session_${Date.now()}`);
  };

  if (loading) {
    return <Loader onLoadComplete={handleLoadComplete} theme={theme} />;
  }

  return (
    <div className={`app ${theme}`}>
      {currentView === 'data' ? (
        <DataViewer
          theme={theme}
          toggleTheme={toggleTheme}
          onClose={() => setCurrentView('chat')}
        />
      ) : currentView === 'knowledge' ? (
        <KnowledgeBase
          theme={theme}
          onClose={() => setCurrentView('chat')}
        />
      ) : (
        <ChatInterface
          theme={theme}
          toggleTheme={toggleTheme}
          onShowData={() => setCurrentView('data')}
          onShowKnowledge={() => setCurrentView('knowledge')}
          messages={chatMessages}
          setMessages={setChatMessages}
          sessionId={sessionId}
          onClearChat={handleClearChat}
        />
      )}
    </div>
  );
}

export default App;
