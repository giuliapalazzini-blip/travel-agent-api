import os

from langchain_core.tools import tool
from serpapi import GoogleSearch
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import Optional
from enum import IntEnum


load_dotenv()


class HotelClassEnum(IntEnum):
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5


class HotelsInput(BaseModel):
    q: str = Field(
        description="Location of the hotel."
    )
    check_in_date: str = Field(
        description="The check-in date (YYYY-MM-DD) e.g. 2024-12-13."
    )
    check_out_date: str = Field(
        description="The check-out date (YYYY-MM-DD) e.g. 2024-12-19."
    )
    adults: Optional[int] = Field(
        1,
        description="The number of adults. Defaults to 1."
    )
    children: Optional[int] = Field(
        0,
        description="The number of children. Defaults to 0."
    )
    hotel_class: Optional[int] = Field(
        2,
        description="The hotel class available from 2 to 5. Defaults to 2."
    )


class HotelsInputSchema(BaseModel):
    params: HotelsInput


@tool(args_schema=HotelsInputSchema)
def hotels_finder(params: HotelsInput):
    """
    This tool uses the SerpApi Google Hotels API to retrieve hotels info.
    """

    search_params = {
        "api_key": os.getenv("SERPAPI_API_KEY"),
        "engine": "google_hotels",
        "hl": "it",
        "gl": "it",
        "currency": "EUR",
        "q": params.q,
        "check_in_date": params.check_in_date,
        "check_out_date": params.check_out_date,
        "adults": params.adults,
        "children": params.children,
        "hotel_class": params.hotel_class,
        "num": 5,
    }

    try:
        print("*" * 80)
        print("hotels_finder")
        print(f"Destinazione: {params.q}")
        print(f"Check-in: {params.check_in_date}")
        print(f"Check-out: {params.check_out_date}")
        print(f"Classe hotel: {params.hotel_class}")
        print("*" * 80)

        search = GoogleSearch(search_params)
        results = search.get_dict()["properties"]

    except Exception as e:
        print("Errore hotels_finder:", e)
        results = str(e)

    return results