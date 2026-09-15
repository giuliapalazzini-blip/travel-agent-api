from datetime import datetime
from typing import Optional
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

TODAY_DATE = datetime.now().strftime("%Y-%m-%d")


class TravelPlanInput(BaseModel):
  start_date: str = Field(
      description=(
          "The start date of the trip (YYYY-MM-DD). Must be on or after today"
          f" ({TODAY_DATE})."
      )
  )
  end_date: str = Field(
      description="The end date of the trip (YYYY-MM-DD)."
  )
  destination: str = Field(description="The destination of the trip.")
  adults: Optional[int] = Field(
      1, description="The number of adults. Defaults to 1."
  )
  children: Optional[int] = Field(
      0, description="The number of children. Defaults to 0."
  )
  travel_style: str = Field(
      description=(
          "The style of travel. e.g. adventure, relax, culture, backpacking,"
          " luxury, family-friendly."
      )
  )
  budget: Optional[int] = Field(
      default=None, description="The total budget for the trip."
  )
  activities: str = Field(
      description=(
          "The preferred activities. e.g. culture, nature, food, shopping."
      )
  )
  food_restriction: str = Field(
      description="Any food restrictions. e.g. vegetarian, gluten-free."
  )


class TravelPlanInputSchema(BaseModel):
  params: TravelPlanInput


class TravelDayOutput(BaseModel):
  day_summary: str = Field(
      description="Brief summary/title of this day of the trip."
  )
  morning: str = Field(description="The activities for the morning.")
  afternoon: str = Field(description="The activities for the afternoon.")
  evening: str = Field(description="The activities for the evening.")


class AccommodationRecommendation(BaseModel):
  hotel_name: str = Field(description="Recommended hotel or accommodation name.")
  description: str = Field(
      description=(
          "Brief description of why it fits the budget and travel style."
      )
  )


class FlightRecommendation(BaseModel):
  flight_details: str = Field(
      description=(
          "Recommended flight option or transport details to destination."
      )
  )


class TravelPlanOutput(BaseModel):
  flight_recommendations: list[FlightRecommendation] = Field(
      description="Flight and transport options for the trip."
  )
  hotel_recommendations: list[AccommodationRecommendation] = Field(
      description="Hotel and accommodation options for the trip."
  )
  travel_plan: list[TravelDayOutput] = Field(
      description="Day-by-day itinerary."
  )


@tool(args_schema=TravelPlanInputSchema)
def chain_travel_plan(params: TravelPlanInput) -> TravelPlanOutput:
  """Generates a comprehensive travel plan based on user input parameters, including flights, hotels, and a day-by-day itinerary."""

  today_str = datetime.now().strftime("%Y-%m-%d")

  print("*" * 80)
  print("chain_travel_plan")
  print(f"Data Odierna: {today_str}")
  print(f"Destinazione: {params.destination}")
  print(f"Periodo: {params.start_date} - {params.end_date}")
  print("*" * 80)

  model = ChatOpenAI(model="gpt-4o")

  system_prompt = f"""
    You are an expert travel agent.
    
    IMPORTANT CONTEXT:
    Today's date is {today_str}. All travel plans, flights, and hotel suggestions MUST be for future dates starting from or after today's date.

    TRIP DETAILS:
    - Destination: {params.destination}
    - Start Date: {params.start_date}
    - End Date: {params.end_date}
    - Adults: {params.adults}
    - Children: {params.children}
    - Travel Style: {params.travel_style}
    - Budget: {params.budget}
    - Preferred Activities: {params.activities}
    - Food Restrictions: {params.food_restriction}

    REQUIREMENTS:
    1. Include realistic flight / transport recommendations suitable for the budget and destination.
    2. Include specific hotel / accommodation recommendations matching the travel style and budget.
    3. Provide a detailed day-by-day itinerary for the duration of the trip.
    
    Use emojis to make your answers engaging, friendly, and structured.
    """

  output_parser = PydanticOutputParser(pydantic_object=TravelPlanOutput)

  prompt = ChatPromptTemplate.from_messages(
      [("human", "{input}\n\n{format_instructions}")]
  )

  chain = prompt | model | output_parser

  result = chain.invoke({
      "input": system_prompt,
      "format_instructions": output_parser.get_format_instructions(),
  })

  print("Piano di viaggio generato correttamente con voli e hotel")

  return result