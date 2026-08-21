from fastapi import APIRouter
from pydantic import BaseModel

from travel_agent_api.services.agent_service import Agent


router = APIRouter()

agent = Agent()


class ChatRequest(BaseModel):
    messages: list


@router.post("/travel-agent")
def travel_agent(request: ChatRequest):
    print("=" * 80)
    print("ROUTE /chat/travel-agent")
    print(f"Messaggi ricevuti: {len(request.messages)}")
    print("=" * 80)

    message = request.messages[-1]["content"]

    response = agent.invoke(message)

    print("Risposta restituita dalla route")
    print("=" * 80)

    return {
        "messages": response["messages"]
    }