
from agents.base import BaseAgent
from utils.hf_manager import get_hf_api_key, query_hf_model_endpoint

class PixelAgent(BaseAgent):
    def __init__(self, model_id="mhbkb/stable-diffusion-xl-base-1.0-text-to-image-1"):
        super().__init__(
            name="Pixel",
            role="Visual Creator (Image Generation)",
            description="Creates all imagery for the project."
        )
        self.hf_api_key = get_hf_api_key()
        if not self.hf_api_key:
            raise ValueError("Hugging Face API key not found in config.yaml.")
        self.default_model_id = model_id
        # Use an uncensored SDXL model (example endpoint)
        self.uncensored_model_id = "Linaqruf/animagine-xl-2.0" 

    def execute_task(self, task):
        """
        Executes an image generation task.

        Args:
            task (dict): A dictionary containing the task details.
                         Expected keys: 'payload'.

        Returns:
            dict: The result from the Hugging Face model endpoint.
        """
        payload = task.get('payload')
        is_nsfw = task.get('is_nsfw', False)

        if not payload:
            raise ValueError("Task must include 'payload'.")

        model_to_use = self.uncensored_model_id if is_nsfw else self.default_model_id

        return query_hf_model_endpoint(self.hf_api_key, model_to_use, payload)
