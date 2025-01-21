from fastapi import APIRouter, HTTPException
from utils import model_utils

router = APIRouter()

from types.schemas import ModelRequest, ModelResponse

@router.post("/download", response_model=ModelResponse)
async def download_model(request: ModelRequest):
    try:
        model_utils.download_model(request.model_name)
        return {"message": f"Model {request.model_name} downloaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/load", response_model=ModelResponse)
async def load_model(request: ModelRequest):
    try:
        model_utils.load_model(request.model_name)
        return {"message": f"Model {request.model_name} loaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/unload", response_model=ModelResponse)
async def unload_model(request: ModelRequest):
    try:
        model_utils.unload_model(request.model_name)
        return {"message": f"Model {request.model_name} unloaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/list", response_model=list[ModelResponse])
async def list_models():
    try:
        models = model_utils.list_models()
        return [{"message": model} for model in models]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
