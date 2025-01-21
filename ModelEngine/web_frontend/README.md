# vLLM Web Frontend

This project provides a web frontend with a chat interface and a model configuration interface for managing models using vLLM and Hugging Face.

## Setup

1. **Activate the virtual environment:**
   ```bash
   source .ModelEngin_venv/bin/activate
   ```

2. **Install the frontend dependencies:**
   ```bash
   npm install react react-dom axios
   ```

3. **Build the frontend:**
   ```bash
   npx webpack --mode development
   ```
   or
   ```bash
   npm run build
   ```

4. **Run the backend:**
   ```bash
   uvicorn backend.main:app --reload
   ```

## Usage

- Open your browser and navigate to `http://localhost:8000`.
- Use the chat interface to send messages.
- Use the model configuration interface to download, load, and unload models.
