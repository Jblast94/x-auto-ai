import asyncio
import logging
from typing import Optional
from telegram import Bot

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class TelegramIntegration:
    """
    Handles posting to Telegram channels as the AI Influencer.
    Requires a valid bot token from @BotFather and the Target Channel ID.
    """
    def __init__(self, token: Optional[str] = None, channel_id: Optional[str] = None):
        self.token = token
        self.channel_id = channel_id
        
        if self.token:
            self.bot = Bot(token=self.token)
        else:
            self.bot = None
            logging.warning("Telegram Bot initialized without a token. It will run in mock mode.")

    async def post_message(self, text: str, image_url: Optional[str] = None) -> dict:
        """Publishes a text (and optional photo) message to the configured channel."""
        if not self.bot or not self.channel_id:
            logging.info(f"[MOCK TELEGRAM] Sending to channel: {text[:50]}...")
            return {"status": "success", "platform_id": "mock_tg_msg_id", "platform": "telegram"}

        try:
            if image_url:
                # If we have media, send media group or photo
                msg = await self.bot.send_photo(chat_id=self.channel_id, photo=image_url, caption=text)
            else:
                msg = await self.bot.send_message(chat_id=self.channel_id, text=text)

            logging.info(f"Successfully posted to Telegram. Message ID: {msg.message_id}")
            return {"status": "success", "platform_id": str(msg.message_id), "platform": "telegram"}
            
        except Exception as e:
            logging.error(f"Failed to post to Telegram: {e}")
            return {"status": "failed", "reason": str(e), "platform": "telegram"}

    async def send_exclusive_paywall(self, teaser_text: str, paywall_url: str) -> dict:
        """Helper to send a teaser + link to OnlyFans/Patreon specifically for monetization."""
        message = f"🔒 **Premium Content Teaser** 🔒\n\n{teaser_text}\n\n👇 See the full uncensored post here:\n{paywall_url}"
        return await self.post_message(message)

if __name__ == "__main__":
    # Test execution
    async def test():
        tg = TelegramIntegration()
        res = await tg.post_message("Hey guys! Just testing my new automated channel! 🚀")
        print(f"Result: {res}")
    
    asyncio.run(test())
