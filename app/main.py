from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from app.core.config import get_settings
from app.api.routes import api_router
from app.services.oddlots import get_oddlots_summary
from app.services.spinoffs import get_spinoffs_summary

settings = get_settings()

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_class=HTMLResponse)
async def root():
    """Get summary of available tickers from both oddlots and spinoffs"""
    oddlots_data = await get_oddlots_summary()
    spinoffs_data = await get_spinoffs_summary()
    
    html_content = """
    <div style="display: flex; gap: 20px; justify-content: center;">
        <div style="border: 1px solid #ccc; padding: 20px; border-radius: 8px;">
            <h2>Oddlots</h2>
            <p>Total Files: {}</p>
            <h3>Tickers:</h3>
            <ul>
                {}
            </ul>
        </div>
        
        <div style="border: 1px solid #ccc; padding: 20px; border-radius: 8px;">
            <h2>Spinoffs</h2>
            <p>Total Files: {}</p>
            <h3>Tickers:</h3>
            <ul>
                {}
            </ul>
        </div>
    </div>
    """
    
    oddlots_tickers = "\n".join([
        f"<li>{t['ticker']} ({t['num_filings']} filings, latest: {t['latest_filing_date']})</li>" 
        for t in oddlots_data["tickers"]
    ])
    
    spinoffs_tickers = "\n".join([
        f"<li>{t['ticker']} ({t['num_filings']} filings, latest: {t['latest_filing_date']})</li>"
        for t in spinoffs_data["tickers"]
    ])
    
    return HTMLResponse(content=html_content.format(
        oddlots_data["total_files"],
        oddlots_tickers,
        spinoffs_data["total_files"],
        spinoffs_tickers
    ))

# Include API routes
app.include_router(api_router, prefix=settings.API_V1_STR)