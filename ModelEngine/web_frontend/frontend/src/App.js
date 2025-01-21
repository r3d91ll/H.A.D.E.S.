import React from 'react';
import ChatInterface from './components/ChatInterface';
import ModelConfigInterface from './components/ModelConfigInterface';

function App() {
    return (
        <div>
            <h1>vLLM Web Frontend</h1>
            <ChatInterface />
            <ModelConfigInterface />
        </div>
    );
}

export default App;
