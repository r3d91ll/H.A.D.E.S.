from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

class ModelStatus(str, Enum):
    DOWNLOADING = "downloading"
    LOADING = "loading"
    READY = "ready"
    UNLOADING = "unloading"
    ERROR = "error"

class ServerStatus(str, Enum):
    STARTING = "starting"
    RUNNING = "running"
    STOPPED = "stopped"
    ERROR = "error"

class ModelRequest(BaseModel):
    model_name: str
    model_path: Optional[str] = None
    gpu_id: Optional[int] = None
    max_gpu_memory: Optional[str] = None

class ModelResponse(BaseModel):
    model_name: str
    status: ModelStatus
    message: Optional[str] = None
    error: Optional[str] = None

class ServerConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int
    model_name: str
    gpu_id: Optional[int] = None
    max_gpu_memory: Optional[str] = None

class ServerResponse(BaseModel):
    server_id: str
    status: ServerStatus
    config: ServerConfig
    error: Optional[str] = None

class ServerList(BaseModel):
    servers: List[ServerResponse]
