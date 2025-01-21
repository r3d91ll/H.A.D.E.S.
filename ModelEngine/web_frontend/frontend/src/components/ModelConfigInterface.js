import React, { useState, useEffect } from 'react';
import axios from 'axios';

function ModelConfigInterface() {
    const [models, setModels] = useState([]);
    const [modelToDownload, setModelToDownload] = useState('');
    const [modelToLoad, setModelToLoad] = useState('');
    const [modelToUnload, setModelToUnload] = useState('');

    useEffect(() => {
        const fetchModels = async () => {
            try {
                const res = await axios.get('/models/list');
                setModels(res.data.map(model => model.message));
            } catch (error) {
                console.error('Error fetching models:', error);
            }
        };

        fetchModels();
    }, []);

    const handleDownload = async (e) => {
        e.preventDefault();
        try {
            await axios.post('/models/download', { model_name: modelToDownload });
            setModelToDownload('');
            alert(`Model ${modelToDownload} downloaded successfully`);
        } catch (error) {
            console.error('Error downloading model:', error);
        }
    };

    const handleLoad = async (e) => {
        e.preventDefault();
        try {
            await axios.post('/models/load', { model_name: modelToLoad });
            setModelToLoad('');
            alert(`Model ${modelToLoad} loaded successfully`);
        } catch (error) {
            console.error('Error loading model:', error);
        }
    };

    const handleUnload = async (e) => {
        e.preventDefault();
        try {
            await axios.post('/models/unload', { model_name: modelToUnload });
            setModelToUnload('');
            alert(`Model ${modelToUnload} unloaded successfully`);
        } catch (error) {
            console.error('Error unloading model:', error);
        }
    };

    return (
        <div>
            <h2>Model Configuration Interface</h2>
            <div>
                <h3>Download Model</h3>
                <form onSubmit={handleDownload}>
                    <input
                        type="text"
                        value={modelToDownload}
                        onChange={(e) => setModelToDownload(e.target.value)}
                        placeholder="Enter model name"
                    />
                    <button type="submit">Download</button>
                </form>
            </div>
            <div>
                <h3>Load Model</h3>
                <form onSubmit={handleLoad}>
                    <input
                        type="text"
                        value={modelToLoad}
                        onChange={(e) => setModelToLoad(e.target.value)}
                        placeholder="Enter model name"
                    />
                    <button type="submit">Load</button>
                </form>
            </div>
            <div>
                <h3>Unload Model</h3>
                <form onSubmit={handleUnload}>
                    <input
                        type="text"
                        value={modelToUnload}
                        onChange={(e) => setModelToUnload(e.target.value)}
                        placeholder="Enter model name"
                    />
                    <button type="submit">Unload</button>
                </form>
            </div>
            <div>
                <h3>Available Models</h3>
                <ul>
                    {models.map((model, index) => (
                        <li key={index}>{model}</li>
                    ))}
                </ul>
            </div>
        </div>
    );
}

export default ModelConfigInterface;
