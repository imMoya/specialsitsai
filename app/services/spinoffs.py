from pathlib import Path
from fastapi import HTTPException
import json
from app.core.config import get_settings

settings = get_settings()

async def get_spinoffs_summary():
    try:
        base_path = Path(settings.BASE_PATH)
        json_path = base_path / "db_spinoffs" / "join_html_mapper.json"
        
        if not json_path.exists():
            raise HTTPException(status_code=404, detail="Mapper file not found")
            
        with open(json_path, 'r') as f:
            data = json.load(f)
            
        return {
            "total_files": len(data),
            "tickers": [
                {
                    "ticker": ticker,
                    "num_filings": len(details["urls"]),
                    "latest_filing_date": max(details["dates_filing"]),
                    "filing_numbers": details["nums_filing"]
                }
                for ticker, details in data.items()
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def get_spinoff_details(ticker: str):
    """Get specific details for a ticker from spinoffs dataset"""
    try:
        base_path = Path(settings.BASE_PATH)
        json_path = base_path / "db_spinoffs" / "join_html_mapper.json"
        
        if not json_path.exists():
            raise HTTPException(status_code=404, detail="Mapper file not found")
            
        with open(json_path, 'r') as f:
            data = json.load(f)
            
        if ticker not in data:
            raise HTTPException(status_code=404, detail=f"Ticker {ticker} not found in spinoffs")
            
        return {
            "dataset": "spinoffs",
            "ticker": ticker,
            "details": data[ticker]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))