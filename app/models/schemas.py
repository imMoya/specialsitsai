from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class TickerInfo(BaseModel):
    ticker: str
    num_filings: int
    latest_filing_date: str
    filing_numbers: List[str]

class DatasetSummary(BaseModel):
    total_files: int
    tickers: List[TickerInfo]

class TickerDetails(BaseModel):
    dataset: str
    ticker: str
    details: dict