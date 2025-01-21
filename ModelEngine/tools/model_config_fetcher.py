#!/usr/bin/env python3
"""
Model Config Fetcher - Fetches the config.json for a specified model from HuggingFace Hub.
"""

import os
import yaml
import json
from pathlib import Path
from huggingface_hub import hf_hub_download, login


def load_config(config_path: str = "model_search_config.yaml") -> dict:
    """Load configuration from YAML file."""
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)


def authenticate_hf():
    """Authenticate with HuggingFace using token from environment."""
    token = os.getenv('HF_TOKEN')
    if not token:
        raise ValueError("HF_TOKEN environment variable not found")
        
    try:
        login(token)
        print("Successfully authenticated with HuggingFace")
    except Exception as e:
        raise Exception(f"Error authenticating: {str(e)}")


def fetch_model_config(model_id: str, output_dir: str = "model_configs") -> str:
    """
    Fetch config.json for the specified model.
    
    Args:
        model_id: The HuggingFace model ID (e.g., 'Qwen/Qwen2.5-Coder-14B-Instruct')
        output_dir: Directory to save the config file
        
    Returns:
        Path to the downloaded config file
    """
    # Create output directory if it doesn't exist
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    try:
        # Download config.json
        config_path = hf_hub_download(
            repo_id=model_id,
            filename="config.json",
            local_dir=output_dir
        )
        
        print(f"\nConfig downloaded to: {config_path}")
        return config_path
        
    except Exception as e:
        raise Exception(f"Error fetching config for {model_id}: {str(e)}")


def display_model_info(config_json: dict):
    """Display relevant model configuration information."""
    print("\nModel Configuration:")
    print("-" * 50)
    
    # Basic model info
    print(f"Base Model: {config_json.get('_name_or_path', 'N/A')}")
    print(f"Architecture: {', '.join(config_json.get('architectures', ['N/A']))}")
    
    # Context length - check various possible keys
    context_length = None
    context_keys = [
        'max_position_embeddings',
        'max_sequence_length',
        'context_window',
        'max_length',
        'n_positions',
        'window_size'
    ]
    
    for key in context_keys:
        if key in config_json:
            context_length = config_json[key]
            print(f"Context Length ({key}): {context_length}")
            break
    
    if context_length is None:
        print("Context length not found in config")
    
    # Other important parameters
    print(f"Hidden Size: {config_json.get('hidden_size', 'N/A')}")
    print(f"Num Attention Heads: {config_json.get('num_attention_heads', 'N/A')}")
    print(f"Num Hidden Layers: {config_json.get('num_hidden_layers', 'N/A')}")
    print(f"Vocabulary Size: {config_json.get('vocab_size', 'N/A')}")
    
    # Save raw config for reference
    print("\nFull config saved to: model_configs/config.json")


def main():
    """Main function to run the config fetcher."""
    try:
        # Authenticate first
        authenticate_hf()
        
        # Load config file
        config = load_config()
        
        # Get model ID from config
        model_id = config.get('target_model')
        if not model_id:
            raise ValueError("No target_model specified in config file")
            
        print(f"\nFetching config for model: {model_id}")
        
        # Fetch the config
        config_path = fetch_model_config(model_id)
        
        # Load and display config information
        with open(config_path, 'r') as f:
            config_json = json.load(f)
            display_model_info(config_json)
            
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        print(traceback.format_exc())


if __name__ == "__main__":
    main()
