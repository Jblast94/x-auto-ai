import os
import random
from typing import Dict, List, Optional
from supabase import create_client, Client
import yaml

class AffiliateManager:
    """
    Manages affiliate marketing links. 
    In a full production environment, this queries the Supabase 'affiliate_links' table.
    For this implementation, it manages a local fallback alongside the DB connection.
    """
    def __init__(self, supabase_client: Optional[Client] = None):
        self.db = supabase_client
        
        # Local fallback library of links by niche/category
        self.local_library = {
            "fitness": [
                {"name": "GymShark Leggings", "url": "https://aff.gymshark.com/ex123", "rate": "10%"},
                {"name": "Optimum Nutrition Whey", "url": "https://amzn.to/opt123", "rate": "5%"}
            ],
            "tech": [
                {"name": "Keychron Keyboard", "url": "https://amzn.to/keychron456", "rate": "4%"},
                {"name": "NordVPN Subscription", "url": "https://nordvpn.com/aff/zoeAI", "rate": "40%"}
            ],
            "lifestyle": [
                {"name": "Curology Skincare", "url": "https://curo.co/aff/glowup", "rate": "$10/signup"},
                {"name": "Stanley Tumbler", "url": "https://amzn.to/stanley789", "rate": "3%"}
            ],
             "general": [
                {"name": "Amazon Prime Free Trial", "url": "https://amzn.to/prime_trial_ai", "rate": "$3/bounty"}
            ]
        }

    async def get_relevant_link(self, niche: str, character_style: str = "general") -> Optional[Dict]:
        """
        Retrieves the best affiliate link for a given post context or character style.
        """
        # Try database first
        if self.db:
            try:
                # Assuming table exists: affiliate_links with columns (id, name, url, category, active)
                result = self.db.table("affiliate_links")\
                    .select("*")\
                    .eq("category", niche)\
                    .eq("active", True)\
                    .execute()
                
                if result.data:
                    return random.choice(result.data)
            except Exception as e:
                print(f"Failed to query Supabase affiliate links: {e}")

        # Fallback to local library
        category = niche.lower() if niche.lower() in self.local_library else character_style.lower()
        if category not in self.local_library:
             category = "general"
             
        links = self.local_library.get(category, [])
        if links:
            return random.choice(links)
            
        return None

    def inject_link(self, text: str, link_data: Dict, platform: str) -> str:
        """
        Appends or injects the affiliate link naturally into the generated text.
        """
        if not link_data:
            return text
            
        url = link_data.get('url', '')
        name = link_data.get('name', 'this product')
        
        # Simple injection logic based on platform
        if platform.lower() in ["x", "twitter"]:
            # Append to end of tweet
            injection = f"\n\nBtw I'm obsessed with {name} right now: {url}"
            # Ensure we don't drastically overflow 280 chars (simplified check)
            if len(text) + len(injection) <= 280:
                return text + injection
            else:
                return text # Too long, omit link
                
        elif platform.lower() == "tiktok":
            # Just add link in bio mention
            return text + f"\n\n(Link for {name} in my bio! 🔗💅)"
            
        else:
            # Default append
            return text + f"\n\nCheck out {name} here: {url}"

# Example Usage
if __name__ == "__main__":
    import asyncio
    
    async def test():
        manager = AffiliateManager()
        link = await manager.get_relevant_link("tech")
        print(f"Selected Link: {link}")
        
        original_tweet = "Just finished building my new PC. The cable management is terrible but it runs so fast! 🤓"
        monetized_tweet = manager.inject_link(original_tweet, link, "x")
        print(f"\nMonetized Tweet:\n{monetized_tweet}")
        
    asyncio.run(test())
