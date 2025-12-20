from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
import asyncpg
from contextlib import asynccontextmanager

# IMPORT YOUR AGENT
from agent import LocalAgent

# --- LIFESPAN MANAGER (The Startup Event) ---
# This allows us to load the heavy AI model ONLY ONCE when the server starts
# instead of reloading it for every single user request.
ai_agent = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Load the AI
    global ai_agent
    print(">>> 🚀 STARTUP: Loading AI Agent...")
    try:
        ai_agent = LocalAgent()
        ai_agent.load_data()
        print(">>> ✅ AI Agent Loaded and Ready!")
    except Exception as e:
        print(f">>> ⚠️ Warning: AI Agent failed to load. Chat will be unavailable. Error: {e}")
    
    yield
    
    # Shutdown: Clean up (if needed)
    print(">>> 🛑 SHUTDOWN: API stopping...")

# --- CONFIGURATION ---
app = FastAPI(
    title="NYC Logistics Platform (AI Powered)",
    version="2.0.0",
    lifespan=lifespan # Connect the startup logic
)

DB_DSN = "postgresql://user:password@localhost:5432/taxidata"

# --- DATA MODELS ---
class LocationMetric(BaseModel):
    location_id: int
    avg_dist: float
    trip_count: int
    avg_cost: Optional[float] = None

class ChatRequest(BaseModel):
    question: str

class ChatResponse(BaseModel):
    answer: str

# --- DATABASE HELPERS ---
async def get_db_connection():
    return await asyncpg.connect(DB_DSN)

# --- ENDPOINTS ---

@app.get("/")
async def health_check():
    return {"status": "online", "ai_status": "ready" if ai_agent else "offline"}

# ... (Keep your existing /metrics endpoints here) ...
@app.get("/metrics/top", response_model=List[LocationMetric])
async def get_top_locations(limit: int = Query(10, ge=1, le=100)):
    conn = await get_db_connection()
    try:
        query = "SELECT location_id, avg_dist, trip_count, avg_cost FROM location_metrics ORDER BY trip_count DESC LIMIT $1"
        rows = await conn.fetch(query, limit)
        return [dict(row) for row in rows]
    finally:
        await conn.close()

# --- NEW: THE CHAT ENDPOINT ---
@app.post("/chat", response_model=ChatResponse)
async def chat_with_data(request: ChatRequest):
    """
    Ask the AI a question about the logistics data.
    """
    if not ai_agent:
        raise HTTPException(status_code=503, detail="AI Agent is not initialized.")
    
    try:
        # We run the synchronous AI code in a way that doesn't block the API
        answer = ai_agent.query(request.question)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))