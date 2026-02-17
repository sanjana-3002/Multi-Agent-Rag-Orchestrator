"""
Backend API for CampaignBrain
FastAPI server exposing multi-agent system
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from Day10.smart_orchestrator import SmartOrchestrator

app = FastAPI(
    title="CampaignBrain API",
    description="Multi-Agent AI System for Marketing Agencies",
    version="1.0.0"
)

# CORS - allow frontend to call API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production: specific domains only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage (in production: use Redis/PostgreSQL)
orchestrators = {}


class QueryRequest(BaseModel):
    query: str
    user_id: str = "demo_user"


class QueryResponse(BaseModel):
    answer: str
    agents_used: List[str]
    execution_time: float
    needs_coordination: bool


class HistoryResponse(BaseModel):
    interactions: List[Dict]
    total: int


@app.get("/")
async def root():
    """Health check"""
    return {
        "status": "healthy",
        "service": "CampaignBrain API",
        "version": "1.0.0"
    }


@app.post("/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    """
    Process user query through multi-agent system
    
    Args:
        request: QueryRequest with query and user_id
    
    Returns:
        QueryResponse with answer and metadata
    """
    
    # Get or create orchestrator for user
    if request.user_id not in orchestrators:
        orchestrators[request.user_id] = SmartOrchestrator(user_id=request.user_id)
    
    orchestrator = orchestrators[request.user_id]
    
    try:
        import time
        start = time.time()
        
        # Execute query
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


@app.get("/history/{user_id}", response_model=HistoryResponse)
async def get_history(user_id: str, limit: int = 10):
    """
    Get conversation history for user
    
    Args:
        user_id: User identifier
        limit: Max number of interactions to return
    
    Returns:
        HistoryResponse with recent interactions
    """
    
    if user_id not in orchestrators:
        return HistoryResponse(interactions=[], total=0)
    
    orchestrator = orchestrators[user_id]
    history = orchestrator.memory.get_recent_history(limit)
    
    return HistoryResponse(
        interactions=history,
        total=len(orchestrator.memory.long_term)
    )


@app.get("/stats/{user_id}")
async def get_stats(user_id: str):
    """Get memory statistics for user"""
    
    if user_id not in orchestrators:
        return {"error": "User not found"}
    
    orchestrator = orchestrators[user_id]
    return orchestrator.memory.get_stats()


@app.delete("/history/{user_id}")
async def clear_history(user_id: str):
    """Clear conversation history for user"""
    
    if user_id in orchestrators:
        orchestrators[user_id].memory.clear_all()
        return {"status": "cleared"}
    
    return {"status": "no history to clear"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)