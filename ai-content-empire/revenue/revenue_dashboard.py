from datetime import datetime, timedelta
from typing import Dict, List
from supabase import create_client, Client
import yaml
import os

class RevenueDashboard:
    def __init__(self, supabase_client: Client):
        self.db = supabase_client
        
    async def get_daily_summary(self) -> Dict:
        """Get today's revenue summary"""
        
        today = datetime.now().date()
        
        result = self.db.rpc('get_daily_revenue_summary', {'start_date': today.isoformat()}).execute()
        
        return {
            "total_revenue": sum(r["total_revenue"] for r in result.data),
            "by_platform": {r["platform"]: r["total_revenue"] for r in result.data},
            "transaction_count": sum(r["transaction_count"] for r in result.data)
        }
    
    async def get_top_content(self, days: int = 7) -> List[Dict]:
        """Get top performing content"""
        
        result = await self.db.table("content_performance").select("""
            content_id,
            platform,
            views,
            likes,
            revenue_generated
        """).gte("created_at", 
            (datetime.now() - timedelta(days=days)).isoformat()
        ).order("revenue_generated", desc=True).limit(10).execute()
        
        return result.data
    
    async def get_revenue_trend(self, days: int = 30) -> List[Dict]:
        """Get revenue trend over time"""
        
        result = await self.db.table("revenue_events").select("""
            created_at,
            amount,
            platform
        """).gte("created_at",
            (datetime.now() - timedelta(days=days)).isoformat()
        ).execute()
        
        # Aggregate by day
        daily = {}
        for r in result.data:
            date = r["created_at"][:10]
            if date not in daily:
                daily[date] = {"total": 0, "count": 0}
            daily[date]["total"] += r["amount"]
            daily[date]["count"] += 1
        
        return [
            {"date": k, "revenue": v["total"], "transactions": v["count"]}
            for k, v in sorted(daily.items())
        ]

if __name__ == '__main__':
    import asyncio

    config_path = os.path.join(os.path.dirname(__file__), '../config/config.yaml')
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)

    supabase_url = config.get('supabase_url')
    supabase_anon_key = config.get('supabase_anon_key')

    if supabase_url and supabase_anon_key:
        supabase: Client = create_client(supabase_url, supabase_anon_key)
        print("Supabase client created successfully.")

        dashboard = RevenueDashboard(supabase)

        async def main():
            daily_summary = await dashboard.get_daily_summary()
            print(f"Daily Summary: {daily_summary}")

            top_content = await dashboard.get_top_content()
            print(f"Top Content: {top_content}")

            revenue_trend = await dashboard.get_revenue_trend()
            print(f"Revenue Trend: {revenue_trend}")

        asyncio.run(main())
    else:
        print("Supabase configuration not found in config.yaml.")
