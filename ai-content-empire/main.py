import asyncio
import logging
import os
import yaml
from supabase import create_client, Client

from content.content_pipeline import ContentPipeline

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def load_config():
    config_path = os.path.join(os.path.dirname(__file__), 'config/config.yaml')
    try:
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        logging.error("Config file not found.")
        return {}

async def main():
    config = load_config()
    supabase_url = config.get('supabase_url')
    supabase_anon_key = config.get('supabase_anon_key')

    if supabase_url and supabase_anon_key:
        logging.info("Initializing Supabase client...")
        supabase: Client = create_client(supabase_url, supabase_anon_key)
        
        logging.info("Initializing ACE Autonomous Pipeline...")
        pipeline = ContentPipeline(supabase)
        
        # Trigger the main DAG cycle
        await pipeline.daily_content_cycle()
        
        logging.info("Run completed successfully.")
    else:
        logging.error("Supabase configuration missing in config.yaml. Cannot proceed.")

if __name__ == "__main__":
    # Ensure correct working directory so relative imports in scripts work
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    asyncio.run(main())
