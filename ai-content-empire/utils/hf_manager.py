import os
import yaml
import requests
from huggingface_hub import HfApi

def get_hf_api_key():
    """Reads the Hugging Face API key from the config file."""
    config_path = os.path.join(os.path.dirname(__file__), '../config/config.yaml')
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    return config.get('hf_api_key')

def list_hf_models(api_key, search=None):
    """Lists models available on the Hugging Face Hub."""
    api = HfApi(token=api_key)
    models = api.list_models(search=search)
    return [model.modelId for model in models]

def list_hf_spaces(api_key):
    """Lists all spaces available on the Hugging Face Hub for the user."""
    api = HfApi(token=api_key)
    spaces = api.list_spaces()
    return [space.id for space in spaces]

def query_hf_model_endpoint(api_key, model_id, payload):
    """Queries a specific Hugging Face model endpoint."""
    headers = {"Authorization": f"Bearer {api_key}"}
    api_url = f"https://api-inference.huggingface.co/models/{model_id}"
    response = requests.post(api_url, headers=headers, json=payload)
    return response.json()

if __name__ == '__main__':
    hf_api_key = get_hf_api_key()
    if hf_api_key:
        print("Hugging Face API key loaded successfully.")
        # Example usage:
        # print("\nListing all models...")
        # all_models = list_hf_models(hf_api_key)
        # print(f"Found {len(all_models)} models.")
        
        # print("\nQuerying a model endpoint...")
        # model_to_query = "gpt2"
        # query_payload = {"inputs": "Hello, my name is"}
        # result = query_hf_model_endpoint(hf_api_key, model_to_query, query_payload)
        # print(f"Query result for {model_to_query}: {result}")
    else:
        print("Hugging Face API key not found in config.yaml.")
