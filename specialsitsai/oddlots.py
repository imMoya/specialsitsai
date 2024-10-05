from typing import Optional, Union
from datetime import datetime
from pydantic import BaseModel, Field
from langchain.output_parsers import DatetimeOutputParser
from langchain_core.output_parsers import StrOutputParser, PydanticOutputParser
from dataclasses import dataclass

class OddLot(BaseModel):
    lower_price: str = Field(description="The currency in which the minimum purchase price per share is denominated.")
    lower_price_currency: str = Field(description="The currency in which the minimum purchase price per share is denominated.")
    higher_price: str = Field(description="What is the highest price in dollars (or other currency) that the company offers to pay per share in this odd-lot tender offer?")
    higher_price_currency: str = Field(description="The currency in which the maximum purchase price per share is denominated.")