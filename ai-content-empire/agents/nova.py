
from agents.base import BaseAgent
from utils.hf_manager import get_hf_api_key, query_hf_model_endpoint

class NovaAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Nova",
            role="Content Creator (Text Generation)",
            description="Generates all written content for various platforms."
        )
        self.hf_api_key = get_hf_api_key()
        if not self.hf_api_key:
            raise ValueError("Hugging Face API key not found in config.yaml.")
            
        # Define default models
        self.default_model = "cognitivecomputations/dolphin-2.9-llama3-8b"
        self.uncensored_model = "cognitivecomputations/dolphin-2.9-llama3-8b" # Dolphin is inherently uncensored/unaligned, but keeping logic separate for flexibility

    def execute_task(self, task):
        """
        Executes a text generation task.

        Args:
            task (dict): A dictionary containing the task details.
                         Expected keys: 'model_id', 'payload'.

        Returns:
            dict: The result from the Hugging Face model endpoint.
        """
        # Override model ID if NSFW is requested
        is_nsfw = task.get('is_nsfw', False)
        
        if is_nsfw:
             model_id = task.get('model_id', self.uncensored_model)
        else:
             model_id = task.get('model_id', self.default_model)
             
        payload = task.get('payload')

        if not payload:
            raise ValueError("Task must include 'payload'.")

        return query_hf_model_endpoint(self.hf_api_key, model_id, payload)

