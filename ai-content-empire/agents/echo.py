import json
import logging
import random
from typing import Dict, List
from datetime import datetime
import requests

from agents.base import BaseAgent
from platforms.x_platform_config import X_ACCOUNTS
from agents.sage import SageAgent
from agents.nova import NovaAgent
from revenue.affiliate_manager import AffiliateManager

from platforms.telegram_bot import TelegramIntegration

class EchoAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Echo",
            role="Engagement & Distribution Manager",
            description="Distributes finalized content to platforms (e.g., X, OnlyFans, Telegram) and tracks engagement."
        )
        # In a real system, these might be passed in, but instantiating locally for this integration
        self.sage = SageAgent()
        
        try:
            self.nova = NovaAgent()
        except:
            self.nova = None # Nova might need HF token handling
            
        self.affiliate_manager = AffiliateManager()
        self.telegram = TelegramIntegration()

    async def execute_task(self, task: dict):
        """
        Executes a distribution task.
        """
        action = task.get("action")
        if action == "publish_content":
            return await self.publish_content(task.get("item"))
        elif action == "listen_for_mentions":
            return await self.listen_for_mentions(task.get("platform", "x"), task.get("character", "luna"))
        else:
            raise ValueError(f"Unknown action for Echo: {action}")

    async def publish_content(self, item: Dict) -> Dict:
        """
        Sends content to the appropriate platform using respective API libraries if configured.
        """
        platform = item.get("platform", "").lower()
        text = item.get("text", "")
        # Get the character context to check for NSFW flags or API keys
        character_name = item.get("character", "default")
        
        if platform in ["x", "twitter"]:
            # Twitter Integration via Tweepy
            logging.info(f"Publishing to Twitter (X): {text[:50]}...")
            # Example Tweepy implementation inside the loop:
            # try:
            #     import tweepy
            #     # Load keys from character JSON or os.environ
            #     client = tweepy.Client(consumer_key=..., consumer_secret=..., access_token=..., access_token_secret=...)
            #     response = client.create_tweet(text=text)
            #     return {"status": "success", "platform_id": response.data['id'], "platform": platform}
            # except Exception as e:
            #     logging.error(f"Tweepy error: {e}")
            
            return {"status": "success", "platform_id": "mock_x_tweet_id_123", "platform": platform}
            
        elif platform == "telegram":
            logging.info(f"Publishing to Telegram: {text[:50]}...")
            # Route to our telegram API wrapper
            return await self.telegram.post_message(text=text)
            
        elif platform == "onlyfans":
            logging.info(f"[MANUAL ACTION REQUIRED] Prepared OnlyFans content: {text[:50]}...")
            logging.info("OnlyFans does not have a public API. This content must be transferred by a scrape-bot or manually via the Web UI Approval Queue.")
            return {"status": "queued_for_manual_upload", "platform_id": "pending", "platform": platform}
            
        else:
            logging.warning(f"Unknown platform specified for distribution: {platform}")
            return {"status": "failed", "reason": f"Unknown platform: {platform}", "platform": platform}

    async def get_engagement(self, platform: str, post_id: str) -> Dict:
        """
        Retrieves engagement metrics for a specific post.
        """
        # Mocking getting metrics
        return {
            "views": 1500,
            "likes": 120,
            "shares": 15,
            "comments": 5
        }

    async def listen_for_mentions(self, platform: str, character_name: str) -> dict:
        """
        Simulates polling an API for recent mentions/comments directed at the influencer.
        In production, this reads from Twitter API/OnlyFans Messaging API endpoints.
        """
        # Simulated incoming message payload
        mock_messages = [
            {"id": "msg1", "user": "@techfan99", "text": "Wow this looks amazing! How do you like the battery life?", "intent": "question"},
            {"id": "msg2", "user": "@gymbro24", "text": "Looking great 💪 What preworkout do you use?", "intent": "question"},
            {"id": "msg3", "user": "@hater01", "text": "AI generated trash.", "intent": "negative"},
        ]
        
        # Simulate fetching 1 random message to respond to
        msg = random.choice(mock_messages)
        logging.info(f"[{self.name}] Detected new mention on {platform} from {msg['user']}: '{msg['text']}'")
        
        response = await self.handle_interaction(msg, character_name, platform)
        return {
            "status": "responded",
            "original_message": msg,
            "response_generated": response
        }
        
    async def handle_interaction(self, message: dict, character_name: str, platform: str) -> str:
        """
        Orchestrates Sage (context) and Nova (text generation) to reply in-character.
        """
        if message["intent"] == "negative":
            # We might ignore trolls
            logging.info(f"[{self.name}] Ignoring negative interaction.")
            return "(Ignored)"
            
        # 1. Ask Sage for character context
        context = await self.sage.execute_task({"action": "get_character_context", "character": character_name})
        traits = context.get('personality', {}).get('traits', [])
        
        # 2. Ask Nova to generate a reply
        prompt = f"Reply to user '{message['user']}' who said: '{message['text']}'. Context: You are {character_name}. Traits: {traits}."
        
        reply_text = ""
        # Try Nova execution, fallback if not initialized/fails
        if self.nova:
            try:
                nova_res = self.nova.execute_task({
                    "model_id": "cognitivecomputations/dolphin-2.9-llama3-8b", 
                    "payload": {"inputs": prompt}
                })
                if isinstance(nova_res, list) and len(nova_res) > 0 and 'generated_text' in nova_res[0]:
                    reply_text = nova_res[0]['generated_text']
            except Exception as e:
                logging.error(f"Echo->Nova generation failed: {e}")
                
        if not reply_text:
            reply_text = f"@{message['user']} Thanks so much!! 🥰 (Fallback Response)"
            
        # 3. Monetization Check (Does this warrant an affiliate link?)
        if "preworkout" in message["text"].lower() or "keyboard" in message["text"].lower():
            link = await self.affiliate_manager.get_relevant_link("general" if not traits else traits[0], character_name)
            if link:
               reply_text = self.affiliate_manager.inject_link(reply_text, link, platform)
               
        logging.info(f"[{self.name}] Sending reply: {reply_text}")
        return reply_text
