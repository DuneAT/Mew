import React, { useState, useEffect, useRef } from 'react';
import ReactMarkdown from 'react-markdown';
import './App.css'; // Importing the CSS file

function App() {
  const [prompt, setPrompt] = useState('');
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [uploadedFiles, setUploadedFiles] = useState([]);
  const [selectedFile, setSelectedFile] = useState(null);
  const [dragging, setDragging] = useState(false);
  const chatEndRef = useRef(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!prompt.trim()) return;

    setMessages((prev) => [...prev, { sender: 'user', text: prompt }]);
    setPrompt('');
    setLoading(true);

    try {
      const res = await fetch('http://localhost:8000/api/ask', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ prompt }),
      });
      const data = await res.json();

      setMessages((prev) => [...prev, { sender: 'ai', text: data.response }]);
    } catch (error) {
      console.error('Error:', error);
      setMessages((prev) => [...prev, { sender: 'ai', text: 'An error occurred. Please try again.' }]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setDragging(true);
  };

  const handleDragLeave = () => {
    setDragging(false);
  };

  const handleDrop = async (e) => {
    e.preventDefault();
    setDragging(false);
    const file = e.dataTransfer.files[0]; // Get the first dropped file

    if (file) {
      const formData = new FormData();
      formData.append('file', file);

      try {
        const response = await fetch('http://localhost:8000/api/upload', {
          method: 'POST',
          body: formData,
        });
        const result = await response.json();
        alert(result.message);

        // Add the file to the uploadedFiles state with its type
        setUploadedFiles((prev) => [
          ...prev,
          { name: file.name, type: file.type || 'unknown' },
        ]);
      } catch (error) {
        console.error('Error uploading file:', error);
      }
    }
  };

  // Helper function to determine the icon based on file type
  const getFileIcon = (type) => {
    if (!type) return '📁'; // Fallback to a generic icon if type is undefined
    if (type.includes('pdf')) return '📄';
    if (type.includes('word') || type.includes('msword') || type.includes('doc')) return '📄';
    if (type.includes('text') || type.includes('plain') || type.includes('txt')) return '📝';
    return '📁'; // Generic icon for other file types
  };

  const handleDeleteFile = async (fileName) => {
    try {
      const response = await fetch(`http://localhost:8000/api/delete-file?file_name=${encodeURIComponent(fileName)}`, {
        method: 'DELETE',
      });
  
      if (response.ok) {
        setUploadedFiles((prev) => prev.filter((file) => file.name !== fileName)); // Remove from UI
        const result = await response.json();
        alert(result.message);
      } else {
        const errorData = await response.json();
        alert(errorData.detail || "Failed to delete the file");
      }
    } catch (error) {
      console.error("Error deleting file:", error);
      alert("Error deleting file.");
    }
  };

  // Scroll to the bottom when messages or loading state changes
  useEffect(() => {
    if (chatEndRef.current) {
      chatEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages, loading]);

  useEffect(() => {
    const fetchFiles = async () => {
      try {
        const response = await fetch("http://localhost:8000/api/list-files");
        const result = await response.json();
        console.log("Fetched files:", result.files); 
        setUploadedFiles(result.files);
      } catch (error) {
        console.error("Error fetching files:", error);
      }
    };
    fetchFiles();
  }, []);
  
  const handleFileClick = (file) => {
    setSelectedFile(file);
  };

  const closePreview = () => {
    setSelectedFile(null);
  };

  return (
    <div className="app-container">
      <div
        className={`chat-container ${dragging ? 'drag-over' : ''}`}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
      >
        <div className="chat-history">
          {messages.map((msg, index) => (
            <div
              key={index}
              className={`chat-message ${msg.sender === 'user' ? 'user-message' : 'ai-message'}`}
            >
              <ReactMarkdown>{msg.text}</ReactMarkdown>
            </div>
          ))}
          {loading && (
            <div className="chat-message ai-message loading-dots">
              <span>.</span><span>.</span><span>.</span>
            </div>
          )}
          <div ref={chatEndRef} />
        </div>

        {/* Display uploaded files with icons and delete button */}
        <div className="uploaded-files">
          {uploadedFiles.map((file, index) => (
            <div key={index} className="uploaded-file">
              <span className="file-icon">{getFileIcon(file.type)}</span>
              <span className="file-name" onClick={() => handleFileClick(file)}>{file.name}</span>
              <span className="delete-icon" onClick={() => handleDeleteFile(file.name)}>❌</span>
            </div>
          ))}
        </div>
      </div>

      <form onSubmit={handleSubmit} className="chat-form">
        <textarea
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Type your message..."
          className="chat-input"
        />
        <button type="submit" className="submit-button">Send</button>
      </form>

      {/* Preview Modal */}
      {selectedFile && (
        <div className="preview-modal">
          <div className="preview-content">
            <button onClick={closePreview} className="close-button">Fermer l'aperçu</button>
            {/* Render preview based on file type */}
            {selectedFile.type && selectedFile.type.includes("image") ? (
              <img src={`http://localhost:8000/uploads/${selectedFile.name}`} alt={selectedFile.name} />
            ) : selectedFile.type && selectedFile.type.includes("pdf") ? (
              <embed src={`http://localhost:8000/uploads/${selectedFile.name}`} type="application/pdf" width="100%" height="500px" />
            ) : (
              <p>Preview not available for this file type.</p>
            )}
          </div>
        </div>
      )}
    </div>
  );
}


export default App;
