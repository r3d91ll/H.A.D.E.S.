import React, { useState } from 'react';
import axios from 'axios';

function ChatInterface() {
    const [message, setMessage] = useState('');
    const [response, setResponse] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const res = await axios.post('/chat/', { message });
            setResponse(res.data.response);
        } catch (error) {
            console.error('Error sending message:', error);
        }
    };

    return (
        <div>
            <h2>Chat Interface</h2>
            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    value={message}
                    onChange={(e) => setMessage(e.target.value)}
                    placeholder="Type your message here"
                />
                <button type="submit">Send</button>
            </form>
            <div>
                <h3>Response:</h3>
                <p>{response}</p>
            </div>
        </div>
    );
}

export default ChatInterface;
