from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import json
from typing import Dict

app = FastAPI(title="SpecialSitsAI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def read_json_mapper(directory: Path) -> Dict:
    """Read and parse the join_html_mapper.json file"""
    json_path = directory / "join_html_mapper.json"
    try:
        if not json_path.exists():
            return {"error": f"Mapper file not found in {json_path}"}
        
        with open(json_path, 'r') as f:
            data = json.load(f)
            
        # Create a summary of available tickers
        return {
            "total_files": len(data),
            "tickers": list(data.keys())
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading mapper: {str(e)}")

@app.get("/")
async def root():
    """Get summary of available tickers from both oddlots and spinoffs"""
    base_path = Path("/Users/ignaciomoyaredondo/Library/CloudStorage/OneDrive-Personal/obsidian/01_projects/secedgarspecial/")
    
    return {
        "oddlots": read_json_mapper(base_path / "db_oddlots"),
        "spinoffs": read_json_mapper(base_path / "db_spinoffs")
    }

@app.get("/details/{dataset}/{ticker}")
async def get_ticker_details(dataset: str, ticker: str):
    """Get specific details for a ticker from either oddlots or spinoffs"""
    base_path = Path("/Users/ignaciomoyaredondo/OneDrive/obsidian/01_projects/secedgarspecial")
    
    if dataset not in ["oddlots", "spinoffs"]:
        raise HTTPException(status_code=400, detail="Dataset must be either 'oddlots' or 'spinoffs'")
    
    json_path = base_path / f"db_{dataset}" / "join_html_mapper.json"
    
    try:
        with open(json_path, 'r') as f:
            data = json.load(f)
            
        if ticker not in data:
            raise HTTPException(status_code=404, detail=f"Ticker {ticker} not found in {dataset}")
            
        return {
            "dataset": dataset,
            "ticker": ticker,
            "details": data[ticker]
        }
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"Mapper file not found for {dataset}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))