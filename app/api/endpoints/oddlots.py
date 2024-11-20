from fastapi import APIRouter, HTTPException
from app.models.schemas import DatasetSummary, TickerDetails
from app.services.oddlots import get_oddlots_summary, get_oddlot_details

router = APIRouter()

@router.get("/", response_model=DatasetSummary)
async def read_oddlots():
    return await get_oddlots_summary()

@router.get("/{ticker}", response_model=TickerDetails)
async def read_oddlot(ticker: str):
    return await get_oddlot_details(ticker)