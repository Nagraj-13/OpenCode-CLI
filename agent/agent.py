from __future__ import annotations
from typing import AsyncGenerator

from agent.events import AgentEvent, AgentEventType
from client.llm_client import LLMClient
from client.response import StreamEventType


class Agent:
    def __init__(self):
        self.client = LLMClient()
    
    async def run(self, message: str):
        yield AgentEvent.agent_start(message)
        # add user message to context
        final_response: str | None = None
        async for event in self._agnetic_loop():
            yield event
            
            if event.type == AgentEventType.TEXT_COMPLETE:
                final_response=event.data.get("content")
        
        yield AgentEvent.agent_end(final_response)
    
    
    async def _agnetic_loop(self)-> AsyncGenerator[AgentEvent, None]:
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hey what is going on"}, 
        ]
        response_text =""
        async for event in self.client.chat_completion(messages,True):
            if event.type == StreamEventType.TEXT_DELTA:
                if event.text_delta:
                    content = event.text_delta.content
                    response_text+=content
                    yield AgentEvent.text_delta(content)
                
            elif event.type == StreamEventType.ERROR:
                yield AgentEvent.agent_error(
                        event.error or "Unknown error occured"
                    )
            # elif event.type == StreamEventType.STREAM_END:
            #     yield AgentEvent.stream_end()
            
        if response_text:
            yield AgentEvent.text_complete(response_text)
            
    
    async def __aenter__(self)-> Agent:
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb,)->None:
        if self.client:
            await self.client.close()
            self.client = None

        