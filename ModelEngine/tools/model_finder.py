#!/usr/bin/env python3
"""
Model Finder - A tool to search for models on Hugging Face Hub based on configurable parameters.
"""

import os
import yaml
from typing import Dict, List, Any
from huggingface_hub import HfApi, login


def load_config(config_path: str = "model_search_config.yaml") -> Dict[str, Any]:
    """Load search configuration from YAML file."""
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)


def authenticate_hf():
    """Authenticate with HuggingFace using token from environment."""
    token = os.getenv('HF_TOKEN')
    if token:
        try:
            login(token)
            print("Successfully authenticated with HuggingFace")
        except Exception as e:
            print(f"Error authenticating: {str(e)}")
    else:
        print("Warning: HF_TOKEN not found in environment variables. Some features may be limited.")


def has_required_keywords(model_info: Dict, config: Dict[str, Any]) -> bool:
    """Check if model has all required keywords in its name or tags."""
    if 'filters' not in config or 'require_all' not in config['filters']:
        return True
        
    required_keywords = [kw.lower() for kw in config['filters']['require_all']]
    model_id = model_info['id'].lower()
    model_tags = [tag.lower() for tag in model_info['tags']]
    pipeline_tags = [tag.lower() for tag in model_info['pipeline_tags']]
    
    # Check each required keyword
    for keyword in required_keywords:
        # Look for keyword in model ID
        found_in_id = keyword in model_id
        
        # Look for keyword in tags
        found_in_tags = any(keyword in tag for tag in model_tags)
        
        # Look for keyword in pipeline tags
        found_in_pipeline = any(keyword in tag for tag in pipeline_tags)
        
        # If keyword wasn't found anywhere, return False
        if not (found_in_id or found_in_tags or found_in_pipeline):
            return False
            
    return True


def check_model_size(model_id: str, min_size: float, max_size: float) -> tuple[bool, float]:
    """Check if model size falls within the specified range. Returns (matches, size)."""
    try:
        # Common size indicators in model names
        size_indicators = ['3b', '7b', '8b', '13b', '14b', '20b', '24b', '32b', '70b']
        model_id_lower = model_id.lower()
        
        for indicator in size_indicators:
            if indicator in model_id_lower:
                size = float(indicator[:-1])
                matches = min_size <= size <= max_size
                return matches, size
                
    except Exception as e:
        print(f"Error checking size for model {model_id}: {str(e)}")
    
    return False, 0


def format_model_info(model: Dict) -> str:
    """Format model information for display."""
    # Try to extract size from model name
    _, size = check_model_size(model['modelId'], 0, float('inf'))
    size_str = f"{size}B" if size > 0 else "Unknown size"
    
    # Format tags more readably
    tags = model.get('tags', [])
    relevant_tags = [tag for tag in tags if any(k in tag.lower() for k in ['code', 'instruct', 'coder'])]
    
    return (
        f"Model: {model['modelId']}\n"
        f"Size: {size_str}\n"
        f"Downloads: {model.get('downloads', 'N/A'):,}\n"
        f"Last Modified: {model.get('lastModified', 'N/A')}\n"
        f"Relevant tags: {', '.join(relevant_tags) if relevant_tags else 'None'}\n"
        f"Pipeline Tags: {', '.join(model.get('pipeline_tags', []))}\n"
        f"-------------------"
    )


def filter_results(models: List[Any], config: Dict[str, Any]) -> List[Dict]:
    """Filter models based on configuration criteria."""
    filtered_models = []
    size_min = config['size'].get('min', 0)
    size_max = config['size'].get('max', float('inf'))
    
    # Get active keywordfilters
    keywordfilters = [k.lower() for k in config.get('keywordfilter', []) if isinstance(k, str)]
    
    print(f"\nFiltering {len(models)} models...")
    print(f"Size range: {size_min}B-{size_max}B")
    print(f"Negative keywords: {keywordfilters}")
    if 'filters' in config and 'require_all' in config['filters']:
        print(f"Required keywords: {config['filters']['require_all']}")
    
    for model in models:
        try:
            # Convert model attributes to a dictionary
            model_info = {
                'id': model.id,
                'modelId': model.id,
                'downloads': getattr(model, 'downloads', 'N/A'),
                'lastModified': getattr(model, 'last_modified', 'N/A'),
                'tags': getattr(model, 'tags', []),
                'pipeline_tags': getattr(model, 'pipeline_tags', [])
            }
            
            model_id = model_info['id'].lower()
            
            # Skip if matches negative keywords
            if any(kf in model_id for kf in keywordfilters):
                continue
                
            # Check size constraints
            matches, size = check_model_size(model_id, size_min, size_max)
            if not matches:
                continue
                
            # Check for required keywords (both instruct and code capabilities)
            if not has_required_keywords(model_info, config):
                continue
            
            # Store the size for sorting
            model_info['size'] = size
            filtered_models.append(model_info)
            
        except Exception as e:
            print(f"Error processing model {getattr(model, 'id', 'unknown')}: {str(e)}")
            continue
    
    # Sort by size and then by downloads
    filtered_models.sort(
        key=lambda x: (
            -x['size'],  # Sort by size descending
            float(x['downloads']) if isinstance(x['downloads'], (int, float, str)) and str(x['downloads']).replace('.','').isdigit() else 0  # Then by downloads
        )
    )
    
    return filtered_models


def main():
    """Main function to run the model search."""
    try:
        # Authenticate with HuggingFace
        authenticate_hf()
        
        # Load configuration
        config = load_config()
        
        # Initialize API
        api = HfApi()
        print("\nSearching for models...")
        
        # Get models with 'instruct' in name or tags
        models = list(api.list_models(
            search="instruct",
            limit=50,
            sort="downloads",
            direction=-1
        ))
        
        # Get models with 'code' in name or tags
        code_models = list(api.list_models(
            search="code",
            limit=50,
            sort="downloads",
            direction=-1
        ))
        
        # Combine and deduplicate
        all_models = list({m.id: m for m in models + code_models}.values())
        print(f"Found {len(all_models)} models before filtering")
        
        # Filter and sort results
        filtered_models = filter_results(all_models, config)
        
        if not filtered_models:
            print("\nNo models found matching all criteria.")
            return
        
        print(f"\nFound {len(filtered_models)} matching models:\n")
        for model in filtered_models:
            print(format_model_info(model))
            
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        import traceback
        print(traceback.format_exc())


if __name__ == "__main__":
    main()
