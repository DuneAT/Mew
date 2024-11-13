import React, { useState } from 'react';
import Chat from '../../components/Chat';
import { sendConversationMessage } from '../../components/commonApi';
import '../../styles/global.css';

const Conversation = () => {
    const [messages, setMessages] = useState([]);
    const [loading, setLoading] = useState(false);

    return (
        <div className="conversation-container">
            <Chat
                messages={messages}
                setMessages={setMessages}
                loading={loading}
                setLoading={setLoading}
            />
        </div>
    );
};

export default Conversation;
