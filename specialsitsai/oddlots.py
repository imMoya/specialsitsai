from typing import Optional, Union
from datetime import datetime
from pydantic import BaseModel, Field
from langchain.output_parsers import DatetimeOutputParser
from langchain_core.output_parsers import StrOutputParser, PydanticOutputParser


class OddLotPrice(BaseModel):
    lower_price: str = Field(description="The currency in which the minimum purchase price per share is denominated.")
    lower_price_currency: str = Field(description="The currency in which the minimum purchase price per share is denominated.")
    higher_price: str = Field(description="What is the highest price in dollars (or other currency) that the company offers to pay per share in this odd-lot tender offer?")
    higher_price_currency: str = Field(description="The currency in which the maximum purchase price per share is denominated.")


class OddLotGeneral(BaseModel):
    oddlot_priority: str = Field(description="A statement indicating whether odd-lot holders are given priority in the tender offer, formatter as True or False")
    shareholder_requirements: str = Field(description="Requirements a shareholder must meet to qualify as an odd-lot holder (e.g., holding fewer than 100 shares).")
    risks: str = Field(description="Identify any conditions or contingencies mentioned in the tender offer that could result in its cancellation. Please, expand in the explanation")
    regulatory_approvals: str = Field(description="List any necessary regulatory approvals or clearances that must be obtained before the tender offer can be completed.")
    tax_consequences: str = Field(description="Description of any potential tax implications for shareholders participating in the offer.")


ODD_LOT_QUESTIONS = {
    "expiration_date": {
        "query": "What is the expiration date of the odd-lot offer?", 
        "parser": DatetimeOutputParser()
    },
    "price": {
        "query": "Please extract the questions from the odd-lot offer", 
        "parser": PydanticOutputParser(pydantic_object=OddLotPrice)
    },
    "general": {
        "query": "Please extract the questions from the odd-lot offer", 
        "parser": PydanticOutputParser(pydantic_object=OddLotGeneral)
    }
}