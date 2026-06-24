import React, { useState } from 'react';
import ChatInterface from './components/ChatInterface';
import DataViewer from './components/DataViewer';
import Loader from './components/Loader';
import './App.css';

function App() {
  const [theme, setTheme] = useState('dark');
  const [showData, setShowData] = useState(false);
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
      {showData ? (
        <DataViewer
          theme={theme}
          toggleTheme={toggleTheme}
          onClose={() => setShowData(false)}
        />
      ) : (
        <ChatInterface
          theme={theme}
          toggleTheme={toggleTheme}
          onShowData={() => setShowData(true)}
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
