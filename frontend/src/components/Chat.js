import React, { useState, useRef, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import '../styles/global.css';

const Chat = ({ apiUrl, messages, setMessages, loading, setLoading }) => {
    const [prompt, setPrompt] = useState('');
    const chatEndRef = useRef(null);

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!prompt.trim()) return;

        setMessages((prev) => [...prev, { sender: 'user', text: prompt }]);
        setPrompt('');
        setLoading(true);

        try {
            const res = await fetch(apiUrl, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ prompt }),
            });
            const data = await res.json();
            setMessages((prev) => [...prev, { sender: 'ai', text: data.response }]);
        } catch (error) {
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

    useEffect(() => {
        if (chatEndRef.current) {
            chatEndRef.current.scrollIntoView({ behavior: 'smooth' });
        }
    }, [messages, loading]);

    return (
        <div className="chat-container">
            <div className="chat-history">
                {messages.map((msg, index) => (
                    <div key={index} className={`chat-message ${msg.sender === 'user' ? 'user-message' : 'ai-message'}`}>
                        <ReactMarkdown>{msg.text}</ReactMarkdown>
                    </div>
                ))}
                {loading && <div className="chat-message ai-message loading-dots"><span>.</span><span>.</span><span>.</span></div>}
                <div ref={chatEndRef} />
            </div>
            <form onSubmit={handleSubmit} className="chat-form">
                <textarea value={prompt} onChange={(e) => setPrompt(e.target.value)} onKeyDown={handleKeyDown} placeholder="Type your message..." className="chat-input" />
                <button type="submit" className="submit-button">Send</button>
            </form>
        </div>
    );
};

export default Chat;
