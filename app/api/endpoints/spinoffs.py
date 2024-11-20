from fastapi import APIRouter, HTTPException
from app.models.schemas import DatasetSummary, TickerDetails
from app.services.spinoffs import get_spinoffs_summary, get_spinoff_details

router = APIRouter()

@router.get("/", response_model=DatasetSummary)
async def read_spinoffs():
    return await get_spinoffs_summary()

@router.get("/{ticker}", response_model=TickerDetails)
async def read_spinoff(ticker: str):
    return await get_spinoff_details(ticker)