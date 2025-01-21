from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import model_routes, server_routes

app = FastAPI(
    title="HADES Model Management API",
    description="API for managing vLLM model servers and configurations",
    version="0.1.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(
    model_routes.router,
    prefix="/api/models",
    tags=["models"]
)

app.include_router(
    server_routes.router,
    prefix="/api/servers",
    tags=["servers"]
)

@app.get("/health")
async def health_check():
    """Simple health check endpoint"""
    return {"status": "healthy"}
