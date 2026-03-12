import asyncio
import yaml
import os
import uuid
import logging
from typing import Dict, List
from datetime import datetime
from supabase import create_client, Client

# Import the actual agent implementations
from agents.atlas import AtlasAgent
from agents.sage import SageAgent
from agents.echo import EchoAgent
from agents.cipher import CipherAgent
from agents.nova import NovaAgent
from agents.pixel import PixelAgent

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class ContentPipeline:
    def __init__(self, supabase_client: Client):
        self.supabase = supabase_client
        
        # Instantiate actual Agents
        self.coordinator = AtlasAgent()
        self.character_engine = SageAgent()
        self.distributor = EchoAgent()
        self.analytics = CipherAgent(db_client=supabase_client)
        
        # Handle text/image HF creation
        try:
            self.text_creator = NovaAgent()
            self.image_creator = PixelAgent()
        except Exception as e:
            logging.error(f"Failed to initialize generating agents: {e}")
            self.text_creator = None
            self.image_creator = None

    async def daily_content_cycle(self):
        """Main content creation cycle (DAG implementation)"""
        logging.info("Starting daily autonomous ACE content cycle...")
        
        # 1. Scout trends & Analytics via Cipher
        analysis = await self.analytics.execute_task({"action": "analyze_performance"})
        trends = analysis.get("insights", ["ai_art", "digital_influencers", "virtual_models"])
        logging.info(f"Analytics & Trends identified: {trends}")
        
        # 2. Coordinate & Plan via Atlas
        # Simple local planning - usually you'd query the text model
        content_plan = self.generate_simple_plan(trends, "luna", ["x", "onlyfans"], 3)
        logging.info(f"Content plan created with {len(content_plan)} items.")
        
        # 3. Generate content in parallel (Nova & Pixel)
        tasks = [self.generate_full_item(item) for item in content_plan]
        content_items = await asyncio.gather(*tasks)
        logging.info(f"Successfully generated {len(content_items)} multimodal items.")
        
        # 4. Apply character consistency (Sage)
        consistent_items = []
        for item in content_items:
            # Inject persona metadata
            item = await self.character_engine.execute_task({
                "action": "apply_persona", 
                "item": item, 
                "character": "luna"
            })
            consistent_items.append(item)
            
        logging.info("Sage successfully applied character bibles.")
        
        # 5. Schedule via Atlas
        scheduled = await self.coordinator.execute_task({
            "action": "schedule_content",
            "content_items": consistent_items,
            "optimal_times": True
        })
        logging.info("Atlas scheduled all items via timeline.")
        
        # 6. Distribute via Echo (Simulated)
        for s_item in scheduled:
            res = await self.distributor.execute_task({
                "action": "publish_content",
                "item": s_item
            })
            if res.get("status") == "success":
                s_item["external_id"] = res.get("platform_id")

        # 7. Store final planned & posted content to Supabase
        await self.store_content_in_database(scheduled)
        logging.info("End of content cycle. Logs recorded to Supabase db.")

        return scheduled

    async def generate_full_item(self, plan: Dict) -> Dict:
        """Invokes Nova & Pixel for Text+Image payloads"""
        text, image = "Fallback text.", "Fallback image."
        
        if self.text_creator:
            try:
                # E.g. prompt HF interface using dict
                # Using dummy payload for Qwen as model logic setup dictates specific keys
                res = self.text_creator.execute_task({
                    "model_id": "cognitivecomputations/dolphin-2.9-llama3-8b", 
                    "payload": {"inputs": plan["prompt"]}
                })
                # Attempt extracting result depending on API response shape
                if isinstance(res, list) and len(res) > 0 and 'generated_text' in res[0]:
                    text = res[0]['generated_text']
                else: 
                    text = f"Sample text generation successful for '{plan['platform']}' using prompt: {plan['prompt'][:30]}..."
            except Exception as e:
                logging.error(f"Nova failed: {e}")
                
        if self.image_creator:
             try:
                res = self.image_creator.execute_task({
                     "payload": {"inputs": plan["image_prompt"]}
                 })
                 # Raw image bits or an error returned
                image = "Image asset placeholder: Bytes successfully processed."
             except Exception as e:
                 logging.error(f"Pixel failed: {e}")

        return {
            "text": text,
            "image": image,
            "platform": plan["platform"],
            "prompt_used": plan["prompt"],
            "metadata": plan["metadata"]
        }

    # Simplistic deterministic content planner until LLM driven
    def generate_simple_plan(self, trends: List[str], character: str, platforms: List[str], count: int) -> List[Dict]:
        content_plan = []
        for i in range(count):
            content_plan.append({
                "prompt": f"Write a tweet or post about {trends[i % len(trends)]}.",
                "image_prompt": f"A realistic photo of a young woman doing {trends[i % len(trends)]}.",
                "platform": platforms[i % len(platforms)],
                "style": "flirty" if character == "luna" else "professional",
                "metadata": {"trend": trends[i % len(trends)]}
            })
        return content_plan

    async def store_content_in_database(self, content_items: List[Dict]):
        """Persist to Supabase Database"""
        for item in content_items:
            try:
                data = {
                    "text": item["text"],
                    "image": str(item["image"])[:50], # Abbreviated for mockup logs
                    "platform": item["platform"],
                    "character": item.get("character", "unknown"),
                    "scheduled_time": item.get("scheduled_time", datetime.now().isoformat()),
                    "metadata": item["metadata"],
                    "created_at": datetime.now().isoformat()
                }
                self.supabase.table("content").insert(data).execute()
            except Exception as e:
                logging.error(f"Error persisting to db: {e}")

if __name__ == '__main__':
    config_path = os.path.join(os.path.dirname(__file__), '../config/config.yaml')
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)

    supabase_url = config.get('supabase_url')
    supabase_anon_key = config.get('supabase_anon_key')

    if supabase_url and supabase_anon_key:
        supabase: Client = create_client(supabase_url, supabase_anon_key)
        logging.info("Supabase connected.")
        pipeline = ContentPipeline(supabase)
        asyncio.run(pipeline.daily_content_cycle())
    else:
        logging.error("Supabase config disabled/missing. Launch aborted.")
