
from hf_manager import get_hf_api_key, list_hf_models

hf_api_key = get_hf_api_key()
if hf_api_key:
    print("Hugging Face API key loaded successfully.")
    print("\nSearching for text-to-image models...")
    models = list_hf_models(hf_api_key, search="text-to-image")
    for model in models:
        print(model)
else:
    print("Hugging Face API key not found in config.yaml.")
