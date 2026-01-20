
import asyncio
import sys
from typing import Any
from agent.agent import Agent
from agent.events import AgentEventType
from client.llm_client import LLMClient
from dotenv import load_dotenv
import click

from ui.tui import TUI, get_console

# Load variables from .env into the environment
load_dotenv()

console = get_console()

class CLI:
    def __init__(self):
        self.agent: Agent | None = None
        self.tui= TUI(console=console)
    
    async def run_single(self, message: str) -> str | None:
        async with Agent() as agent:
            self.agent= agent
            return await self._process_message(message)
 
    async def _process_message(self, message: str):
        if not self.agent:
            return None
        
        assistant_streaming = False
        final_response : str | None=None
        async for event in self.agent.run(message):
            if event.type == AgentEventType.TEXT_DELTA:
                content = event.data.get("content", "")
                if not assistant_streaming:
                    self.tui.begin_assistant()
                    assistant_streaming = True
                self.tui.stream_assistant_delta(content)
            elif event.type == AgentEventType.TEXT_COMPLETE:
                final_response = event.data.get("content", "")
                if assistant_streaming:
                    self.tui.end_assistant()
                    assistant_streaming=False
            elif event.type == AgentEventType.AGENT_ERROR:
                error = event.data.get("error", "Unknown Error")
                details = event.data.get("details", "")
                console.print(f"\n[error]Error: {error}[/error]")
                console.print(f"\n[error]Details: {details}[/error]")
                
                 
        return final_response




async def run(messages: dict[str, Any]):
    client = LLMClient()
    async for event in client.chat_completion(messages,True):
        print(event)

@click.command()
@click.argument("prompt", required=False)
def main(
    prompt: str | None
):
    cli = CLI()
    # messages = [
    #     {"role": "system", "content": "You are a helpful assistant."},
    #     {"role": "user", "content": prompt}, 
    # ]
    if prompt: 
        result = asyncio.run(cli.run_single(prompt))
        if result is None:
            sys.exit(1)
    

main()