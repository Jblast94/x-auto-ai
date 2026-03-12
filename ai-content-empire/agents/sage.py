import json
import os
from typing import Dict

from agents.base import BaseAgent

class SageAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Sage",
            role="Character Engine",
            description="Maintains character consistency by applying character bibles to generated content."
        )
        self.bibles_dir = os.path.join(os.path.dirname(__file__), '../content/character_bibles')

    def load_character(self, character_name: str) -> dict:
        """
        Loads the character bible JSON.
        """
        try:
            file_path = os.path.join(self.bibles_dir, f"{character_name.lower()}.json")
            with open(file_path, 'r') as f:
                return json.load(f).get('character', {})
        except FileNotFoundError:
            # Fallback barebones character if not found
            return {"name": character_name, "personality": {"traits": ["generic"]}, "style": "neutral"}
        except json.JSONDecodeError as e:
            print(f"Error decoding character bible for {character_name}: {e}")
            return {"name": character_name}

    async def execute_task(self, task: dict):
        """
        Executes a character consistency task.
        """
        action = task.get("action")
        if action == "apply_persona":
            item = task.get("item")
            character_name = task.get("character", "luna")
            return await self.apply_persona(item, character_name)
        elif action == "get_character_context":
            return self.load_character(task.get("character", "luna"))
        else:
            raise ValueError(f"Unknown action for Sage: {action}")

    async def apply_persona(self, item: Dict, character_name: str) -> Dict:
        """
        Ensures the content item tags and metadata are aligned with the character.
        If we were using an LLM here, we could re-write the text. 
        For now, we inject character context metadata.
        """
        character_data = self.load_character(character_name)
        
        # Inject character metadata into the item
        item["character"] = character_name
        if "metadata" not in item:
            item["metadata"] = {}
            
        item["metadata"]["character_traits"] = character_data.get("personality", {}).get("traits", [])
        
        # In a fully LLM-driven mode, Sage would call the text generation model again
        # here to rewrite `item['text']` to perfectly match `character_data['speech_patterns']`.
        
        return item
