from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

from travel_agent_api.tools.flights_finder import flights_finder
from travel_agent_api.tools.hotels_finder import hotels_finder
from travel_agent_api.tools.chain_travel_plan import chain_travel_plan
from travel_agent_api.tools.chain_historical_expert import chain_historical_expert


class Agent:
    def __init__(self):
        print("*" * 80)
        print("Inizializzazione Travel Agent")
        print("*" * 80)

        self.model = ChatOpenAI(
            model="gpt-4o",
            temperature=0
        )

        self.tools = [
            flights_finder,
            hotels_finder,
            chain_travel_plan,
            chain_historical_expert,
        ]

        self.agent = create_react_agent(
            model=self.model,
            tools=self.tools,
        )

        print("Travel Agent inizializzato correttamente")

    def invoke(self, message: str):
        print("*" * 80)
        print("Agent.invoke")
        print(f"Messaggio ricevuto: {message}")
        print("*" * 80)

        result = self.agent.invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": message,
                    }
                ]
            }
        )

        print("Esecuzione Agent completata")

        return result