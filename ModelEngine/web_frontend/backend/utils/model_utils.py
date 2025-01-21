import os
import subprocess

MODELS_DIR = "models"

def download_model(model_name: str):
    if not os.path.exists(MODELS_DIR):
        os.makedirs(MODELS_DIR)
    subprocess.run(["vllm", "download", model_name, "--output-dir", MODELS_DIR], check=True)

def load_model(model_name: str):
    subprocess.run(["vllm", "load", model_name], check=True)

def unload_model(model_name: str):
    subprocess.run(["vllm", "unload", model_name], check=True)

def list_models():
    if not os.path.exists(MODELS_DIR):
        return []
    return [name for name in os.listdir(MODELS_DIR) if os.path.isdir(os.path.join(MODELS_DIR, name))]
