import asyncio
import sys
import os

# Ensure project root is in path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from agents.echo import EchoAgent

async def test_echo_interaction():
    print("Initializing Echo Agent for interaction test...")
    echo = EchoAgent()
    
    print("\n--- Triggering Simulated Mention ---")
    result = await echo.execute_task({
        "action": "listen_for_mentions",
        "platform": "x",
        "character": "luna"
    })
    
    print("\n--- Result ---")
    print(f"Message Intended: {result['original_message']['text']}")
    print(f"Generated Response: {result['response_generated']}")

if __name__ == "__main__":
    asyncio.run(test_echo_interaction())
