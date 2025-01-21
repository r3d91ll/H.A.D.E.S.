# HADES Web Frontend

This is the web frontend for the HADES (Highly Advanced Distributed Execution System) project. It provides a web interface for managing vLLM model servers and configurations.

## Backend Structure

The backend is built with FastAPI and provides the following features:
- Model management (download, load, unload)
- Server management (start, stop, health check)
- Type-safe API with Pydantic models
- Async operations for better performance

### API Endpoints

#### Models
- `POST /api/models/download` - Download a model from Hugging Face
- `POST /api/models/load` - Load a model into vLLM
- `POST /api/models/unload` - Unload a model from vLLM
- `GET /api/models/list` - List all active models

#### Servers
- `POST /api/servers/start` - Start a new vLLM server instance
- `POST /api/servers/stop/{server_id}` - Stop a running server
- `GET /api/servers/list` - List all server instances
- `GET /api/servers/health/{server_id}` - Check server health

## Setup

1. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Start the backend server:
```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8080
```

4. Access the API documentation at:
- Swagger UI: http://localhost:8080/docs
- ReDoc: http://localhost:8080/redoc

## Development

The backend follows these principles:
- Full type hints and Pydantic models
- Async-first approach
- Clean separation of concerns
- Easy to test and maintain

### Adding New Features

1. Add new schemas in `backend/types/schemas.py`
2. Implement utility functions in `backend/utils/`
3. Create new routes in `backend/routers/`
4. Update main.py to include new routers
