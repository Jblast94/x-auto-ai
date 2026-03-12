import json
import os
from datetime import datetime, timedelta
from typing import Dict, List

from agents.base import BaseAgent

class AtlasAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Atlas",
            role="Project Coordinator",
            description="Manages the content pipeline, schedules tasks, and coordinates other agents."
        )

    async def execute_task(self, task: dict):
        """
        Executes a scheduling or coordination task.
        """
        action = task.get("action")
        if action == "schedule_content":
            return await self.schedule_content(task.get("content_items", []), task.get("optimal_times", True))
        elif action == "generate_daily_briefing":
            return await self.generate_daily_briefing()
        else:
            raise ValueError(f"Unknown action for Atlas: {action}")

    async def schedule_content(self, content_items: List[Dict], optimal_times: bool = True) -> List[Dict]:
        """
        Assigns timestamps to content items for distribution.
        """
        scheduled_items = []
        base_time = datetime.now()
        
        # Simple scheduling logic: distribute evenly over the next 12 hours
        interval = timedelta(hours=12 / max(len(content_items), 1))
        
        for i, item in enumerate(content_items):
            if optimal_times:
                # In a real scenario, query Cipher for best times. For now, space them out.
                scheduled_time = base_time + (interval * (i+1))
            else:
                scheduled_time = base_time + timedelta(minutes=(i * 30))
                
            item["scheduled_time"] = scheduled_time.isoformat()
            scheduled_items.append(item)
            
        return scheduled_items

    async def generate_daily_briefing(self) -> str:
        """
        Generates a summary of planned activities for the day.
        """
        today = datetime.now().strftime("%Y-%m-%d")
        return f"Daily Briefing for {today}: Agents initialized. Pipeline ready."
