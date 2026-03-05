from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any

from backend.core.sql_generator import SQLGenerator
from backend.core.memory import ConversationMemory
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(title="Hybrid NL2SQL Chat API", version="1.0.0")

# Instantiate instances
# No global instance, we create it per-request now to handle dynamic API keys

class ChatRequest(BaseModel):
    query: str
    api_key: str | None = None

class ChatResponse(BaseModel):
    query: str
    complexity: str
    generated_sql: Optional[str] = None
    reasoning: Optional[str] = None
    explanation: Optional[str] = None
    results: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

@app.get("/")
async def root():
    """Root endpoint to show the backend is active."""
    return {
        "status": "HNV AI Backend Running",
        "endpoints": ["/chat", "/status", "/stats"]
    }

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """Main endpoint handling NLQ natural language queries."""
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty.")
        
    try:
        # Generate, validate, and execute the SQL query via the core logic
        # Initialize generator with the user's key for this specific request
        generator = SQLGenerator(api_key=request.api_key)
        result = generator.generate_and_execute(request.query)
        
        return ChatResponse(
            query=request.query,
            complexity=result.get("complexity", "UNKNOWN"),
            generated_sql=result.get("generated_sql"),
            reasoning=result.get("reasoning"),
            explanation=result.get("explanation"),
            results=result.get("results"),
            error=result.get("error")
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/status")
async def get_status():
    """Endpoint to check if the backend has an API key configured."""
    has_key = os.getenv("GEMINI_API_KEY") is not None and os.getenv("GEMINI_API_KEY") != ""
    return {"api_configured": has_key}

@app.get("/stats")
async def get_db_stats():
    """Endpoint to get live record counts for the dashboard."""
    from backend.core.db_connector import DBConnector
    db = DBConnector()
    stats = {}
    for table in ["employees", "students", "projects", "departments"]:
        res = db.execute_query(f"SELECT COUNT(*) as count FROM {table}")
        stats[table] = res["rows"][0][0] if not res.get("error") else 0
    return stats

@app.delete("/memory")
async def clear_memory():
    """Endpoint to clear the session memory context."""
    # Memory is managed by the ConversationMemory class
    from backend.core.memory import ConversationMemory
    ConversationMemory().clear()
    return {"status": "Memory Cleared"}

if __name__ == "__main__":
    import uvicorn
    # Final port for stability
    uvicorn.run(app, host="127.0.0.1", port=8080)
