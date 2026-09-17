from fastapi import APIRouter
from pydantic import BaseModel, Field

from travel_agent_api.services.agent_service import Agent


router = APIRouter()

agent = Agent()


class ChatMessage(BaseModel):
    role: str = Field(min_length=1)
    content: str = Field(min_length=1)


class ChatRequest(BaseModel):
    messages: list[ChatMessage] = Field(min_length=1)


@router.post("/travel-agent")
def travel_agent(request: ChatRequest):
    print("=" * 80)
    print("ROUTE /chat/travel-agent")
    print(f"Messaggi ricevuti: {len(request.messages)}")
    print("=" * 80)

    messages = [
        message.model_dump()
        for message in request.messages
    ]

    response = agent.invoke(messages)

    print("Risposta restituita dalla route")
    print("=" * 80)

    return {
        "messages": response["messages"]
    }