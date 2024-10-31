import React, { useState } from 'react';
import './App.css';

function App() {
  const [prompt, setPrompt] = useState('');
  const [chatHistory, setChatHistory] = useState([]);
  const [darkMode, setDarkMode] = useState(false);

  const toggleDarkMode = () => {
    setDarkMode(!darkMode);
    document.body.classList.toggle("dark-mode", !darkMode);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Add user's prompt to chat history
    setChatHistory([...chatHistory, { sender: 'user', text: prompt }]);
    
    // Send the prompt to the backend
    const res = await fetch('http://localhost:8000/api/ask', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ prompt }),
    });

    const data = await res.json();
    const responseText = data.response;

    // Add the response from LLM to chat history
    setChatHistory(prevHistory => [
      ...prevHistory,
      { sender: 'response', text: responseText }
    ]);
    
    // Clear prompt input
    setPrompt('');
  };

  return (
    <div className="App">
      <button onClick={toggleDarkMode}>
        {darkMode ? 'Switch to Day Mode' : 'Switch to Night Mode'}
      </button>

      <div className="chat-history">
        {chatHistory.map((msg, index) => (
          <div
            key={index}
            className={`chat-message ${msg.sender === 'user' ? 'user' : 'response'}`}
          >
            {msg.text}
          </div>
        ))}
      </div>

      <form onSubmit={handleSubmit}>
        <textarea
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="Enter your prompt"
          rows="3"
        />
        <button type="submit">Ask</button>
      </form>
    </div>
  );
}

export default App;
