import asyncio
import json
import os
import uuid
from typing import Dict, List, Optional
from ..types.schemas import ServerConfig, ServerResponse, ServerStatus

class ServerManager:
    def __init__(self):
        self.servers: Dict[str, ServerResponse] = {}
        self.processes: Dict[str, asyncio.subprocess.Process] = {}

    async def start_server(self, config: ServerConfig) -> ServerResponse:
        """Start a new vLLM server instance"""
        server_id = str(uuid.uuid4())
        
        try:
            # Create server response object
            server = ServerResponse(
                server_id=server_id,
                status=ServerStatus.STARTING,
                config=config
            )
            self.servers[server_id] = server

            # Construct vLLM command
            cmd = [
                "python", "-m", "vllm.entrypoints.openai.api_server",
                "--host", config.host,
                "--port", str(config.port),
                "--model", config.model_name
            ]
            
            if config.gpu_id is not None:
                cmd.extend(["--gpu", str(config.gpu_id)])
            if config.max_gpu_memory:
                cmd.extend(["--max-gpu-memory", config.max_gpu_memory])

            # Start server process
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            self.processes[server_id] = process
            self.servers[server_id].status = ServerStatus.RUNNING
            
            return self.servers[server_id]
        
        except Exception as e:
            if server_id in self.servers:
                self.servers[server_id].status = ServerStatus.ERROR
                self.servers[server_id].error = str(e)
            raise

    async def stop_server(self, server_id: str) -> ServerResponse:
        """Stop a running vLLM server instance"""
        if server_id not in self.servers:
            raise ValueError(f"Server {server_id} not found")
        
        try:
            # Get process
            process = self.processes.get(server_id)
            if process:
                process.terminate()
                await process.wait()
                del self.processes[server_id]
            
            # Update server status
            self.servers[server_id].status = ServerStatus.STOPPED
            return self.servers[server_id]
        
        except Exception as e:
            self.servers[server_id].status = ServerStatus.ERROR
            self.servers[server_id].error = str(e)
            raise

    def list_servers(self) -> List[ServerResponse]:
        """List all server instances and their status"""
        return list(self.servers.values())

    async def check_server_health(self, server_id: str) -> ServerResponse:
        """Check if a server is healthy and responding"""
        if server_id not in self.servers:
            raise ValueError(f"Server {server_id} not found")
        
        server = self.servers[server_id]
        process = self.processes.get(server_id)
        
        if not process:
            server.status = ServerStatus.STOPPED
            return server
        
        # Check if process is still running
        if process.returncode is not None:
            server.status = ServerStatus.ERROR
            server.error = "Server process terminated unexpectedly"
        else:
            # TODO: Implement actual health check by making a request to the server
            server.status = ServerStatus.RUNNING
        
        return server
