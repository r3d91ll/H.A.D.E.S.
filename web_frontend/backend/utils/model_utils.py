import json
import os
from typing import List, Dict, Optional
from ..types.schemas import ModelStatus, ModelResponse
from pathlib import Path

class ModelManager:
    def __init__(self, model_dir: str = "./model_configs"):
        self.model_dir = model_dir
        self.active_models: Dict[str, ModelResponse] = {}
        self.hf_cache_dir = os.path.expanduser("~/.cache/huggingface/hub/models--*")
        self._load_active_models()
        self._discover_cached_models()

    def _load_active_models(self):
        """Load active models from configuration file"""
        config_file = os.path.join(self.model_dir, "active_models.json")
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                data = json.load(f)
                for model_data in data:
                    self.active_models[model_data["model_name"]] = ModelResponse(**model_data)

    def _discover_cached_models(self):
        """Discover models from HuggingFace cache directory"""
        import glob
        
        # Find all model directories
        model_dirs = glob.glob(self.hf_cache_dir)
        
        for model_dir in model_dirs:
            # Extract model name from directory path
            # Format: models--owner--model_name
            parts = os.path.basename(model_dir).split('--')
            if len(parts) >= 3:
                owner = parts[1]
                model_name = '--'.join(parts[2:])  # Handle model names with dashes
                full_name = f"{owner}/{model_name}"
                
                # Add to active models if not already present
                if full_name not in self.active_models:
                    self.active_models[full_name] = ModelResponse(
                        model_name=full_name,
                        status=ModelStatus.READY,
                        message="Found in cache"
                    )
        
        # Save discovered models
        self._save_active_models()

    def _save_active_models(self):
        """Save current active models to configuration file"""
        config_file = os.path.join(self.model_dir, "active_models.json")
        os.makedirs(os.path.dirname(config_file), exist_ok=True)
        with open(config_file, 'w') as f:
            json.dump([model.dict() for model in self.active_models.values()], f, indent=2)

    async def download_model(self, model_name: str) -> ModelResponse:
        """Download a model from Hugging Face"""
        try:
            # Update status to downloading
            self.active_models[model_name] = ModelResponse(
                model_name=model_name,
                status=ModelStatus.DOWNLOADING
            )
            
            # TODO: Implement actual model download logic
            # For now, just simulate success
            self.active_models[model_name].status = ModelStatus.READY
            self._save_active_models()
            
            return self.active_models[model_name]
        except Exception as e:
            self.active_models[model_name] = ModelResponse(
                model_name=model_name,
                status=ModelStatus.ERROR,
                error=str(e)
            )
            raise

    async def load_model(self, model_name: str, gpu_id: Optional[int] = None) -> ModelResponse:
        """Load a model into vLLM"""
        try:
            # Update status to loading
            self.active_models[model_name] = ModelResponse(
                model_name=model_name,
                status=ModelStatus.LOADING
            )
            
            # TODO: Implement actual model loading logic with vLLM
            # For now, just simulate success
            self.active_models[model_name].status = ModelStatus.READY
            self._save_active_models()
            
            return self.active_models[model_name]
        except Exception as e:
            self.active_models[model_name] = ModelResponse(
                model_name=model_name,
                status=ModelStatus.ERROR,
                error=str(e)
            )
            raise

    async def unload_model(self, model_name: str) -> ModelResponse:
        """Unload a model from vLLM"""
        try:
            if model_name not in self.active_models:
                raise ValueError(f"Model {model_name} not found")
            
            # Update status to unloading
            self.active_models[model_name].status = ModelStatus.UNLOADING
            
            # TODO: Implement actual model unloading logic
            # For now, just remove from active models
            del self.active_models[model_name]
            self._save_active_models()
            
            return ModelResponse(
                model_name=model_name,
                status=ModelStatus.READY,
                message="Model unloaded successfully"
            )
        except Exception as e:
            return ModelResponse(
                model_name=model_name,
                status=ModelStatus.ERROR,
                error=str(e)
            )

    def list_models(self) -> List[ModelResponse]:
        """List all active models and their status"""
        return list(self.active_models.values())
