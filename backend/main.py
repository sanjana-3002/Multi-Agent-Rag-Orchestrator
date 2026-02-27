"""
Backend API for CampaignBrain
FastAPI server exposing multi-agent system
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
import os
from dotenv import load_dotenv

load_dotenv()

# Import from local backend folder (not Day10)
try:
    from smart_orchestrator import SmartOrchestrator
except ImportError:
    # Fallback: create a simple mock orchestrator
    class SmartOrchestrator:
        def __init__(self, user_id="demo"):
            self.user_id = user_id
        
        def execute(self, query):
            return {
                "answer": f"Received query: {query}. Backend is running!",
                "agents_used": ["demo"],
                "needs_coordination": False
            }

app = FastAPI(
    title="CampaignBrain API",
    description="Multi-Agent AI System",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

orchestrators = {}


class QueryRequest(BaseModel):
    query: str
    user_id: str = "demo_user"


class QueryResponse(BaseModel):
    answer: str
    agents_used: List[str]
    execution_time: float
    needs_coordination: bool


@app.get("/")
async def root():
    """Health check"""
    return {
        "status": "healthy",
        "service": "CampaignBrain API",
        "version": "1.0.0",
        "environment": "production"
    }


@app.get("/demo/company/{ticker}")
async def demo_company(ticker: str):
    """Demo endpoint with real data"""
    try:
        from tools.financial_data import get_company_financials
        from tools.news_data import get_company_news
        
        financial = get_company_financials(ticker)
        news = get_company_news(ticker)
        
        return {
            "ticker": ticker,
            "financial_data": financial,
            "news_data": news,
            "powered_by": "Real-time APIs"
        }
    except Exception as e:
        return {
            "ticker": ticker,
            "error": str(e),
            "note": "Make sure API keys are set in environment variables"
        }


@app.post("/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    """Process query through multi-agent system"""
    
    if request.user_id not in orchestrators:
        orchestrators[request.user_id] = SmartOrchestrator(user_id=request.user_id)
    
    orchestrator = orchestrators[request.user_id]
    
    try:
        import time
        start = time.time()
        
        result = orchestrator.execute(request.query)
        execution_time = time.time() - start
        
        return QueryResponse(
            answer=result.get("answer", "No answer generated"),
            agents_used=result.get("agents_used", []),
            execution_time=execution_time,
            needs_coordination=result.get("needs_coordination", False)
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
