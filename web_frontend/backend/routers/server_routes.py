from fastapi import APIRouter, HTTPException
from typing import List
from ..types.schemas import ServerConfig, ServerResponse, ServerList
from ..utils.server_utils import ServerManager

router = APIRouter()
server_manager = ServerManager()

@router.post("/start", response_model=ServerResponse)
async def start_server(config: ServerConfig):
    """Start a new vLLM server instance"""
    try:
        return await server_manager.start_server(config)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/stop/{server_id}", response_model=ServerResponse)
async def stop_server(server_id: str):
    """Stop a running vLLM server instance"""
    try:
        return await server_manager.stop_server(server_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/list", response_model=ServerList)
async def list_servers():
    """List all server instances and their status"""
    try:
        servers = server_manager.list_servers()
        return ServerList(servers=servers)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health/{server_id}", response_model=ServerResponse)
async def check_server_health(server_id: str):
    """Check if a server is healthy and responding"""
    try:
        return await server_manager.check_server_health(server_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
