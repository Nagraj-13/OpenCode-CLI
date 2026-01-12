
import asyncio
from client.llm_client import LLMClient
from dotenv import load_dotenv

# Load variables from .env into the environment
load_dotenv()

async def main():
    client = LLMClient()
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Whats up"}, 
    ]
    async for event in client.chat_completion(messages,True):
        print(event)
    
if __name__ == "__main__":
    asyncio.run(main())