from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field


class HistoricalExpertInput(BaseModel):
    location: str = Field(
        description="The city or historical location to analyze."
    )


class HistoricalExpertInputSchema(BaseModel):
    params: HistoricalExpertInput


@tool(args_schema=HistoricalExpertInputSchema)
def chain_historical_expert(params: HistoricalExpertInput):
    """
    Provides historical and cultural information about a destination.
    """

    print("*" * 80)
    print("chain_historical_expert")
    print(f"Località: {params.location}")
    print("*" * 80)

    model = ChatOpenAI(model="gpt-4o")

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
                You are an expert in history, art and culture.

                Provide useful historical and cultural information
                about the requested destination.

                Explain the most important monuments, historical events,
                cultural characteristics and interesting facts.

                Use clear language and make the answer useful for a traveler.
                """
            ),
            (
                "human",
                "{location}"
            )
        ]
    )

    chain = prompt | model

    result = chain.invoke(
        {
            "location": params.location
        }
    )

    print("Informazioni storiche generate correttamente")

    return result.content