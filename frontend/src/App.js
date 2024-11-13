import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HomePage from './pages/Homepage';
import Conversation from './tools/Conversation/conversationPage';
import RAG from './tools/rag/ragPage';
import NotFound from './pages/NotFound';
import './styles/global.css';

function App() {
    return (
        <Router>
            <div className="app-container">
                {/* Optional: Navbar or other shared layout components */}
                <Routes>
                    <Route path="/" element={<HomePage />} />
                    <Route path="/conversation" element={<Conversation />} />
                    <Route path="/rag" element={<RAG />} />
                    <Route path="*" element={<NotFound />} />
                </Routes>
                {/* Optional: Footer component */}
            </div>
        </Router>
    );
}

export default App;