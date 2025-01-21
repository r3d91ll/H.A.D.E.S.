from fastapi import APIRouter, HTTPException, Depends
from typing import List
from ..types.schemas import ModelRequest, ModelResponse
from ..utils.model_utils import ModelManager

router = APIRouter()
model_manager = ModelManager()

@router.post("/download", response_model=ModelResponse)
async def download_model(request: ModelRequest):
    """Download a model from Hugging Face"""
    try:
        return await model_manager.download_model(request.model_name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/load", response_model=ModelResponse)
async def load_model(request: ModelRequest):
    """Load a model into vLLM"""
    try:
        return await model_manager.load_model(
            request.model_name,
            gpu_id=request.gpu_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/unload", response_model=ModelResponse)
async def unload_model(request: ModelRequest):
    """Unload a model from vLLM"""
    try:
        return await model_manager.unload_model(request.model_name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/list", response_model=List[ModelResponse])
async def list_models():
    """List all active models and their status"""
    try:
        return model_manager.list_models()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
