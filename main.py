from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
import asyncpg

# --- CONFIGURATION ---
app = FastAPI(
    title="NYC Logistics API",
    description="High-performance API to serve taxi trip analytics.",
    version="1.0.0"
)

# Database Connection String (Same as Project 01)
DB_DSN = "postgresql://user:password@localhost:5432/taxidata"

# --- DATA MODELS (The "Contract") ---
# This defines exactly what the data looks like. 
# It serves as both documentation and validation.
class LocationMetric(BaseModel):
    location_id: int
    avg_dist: float
    trip_count: int
    avg_cost: Optional[float] = None # Optional field

# --- DATABASE HELPERS ---
async def get_db_connection():
    """Establishes an asynchronous connection to PostgreSQL."""
    # We use 'asyncpg' because it is much faster than standard drivers
    return await asyncpg.connect(DB_DSN)

# --- API ENDPOINTS ---

@app.get("/")
async def health_check():
    """Simple check to see if the API is running."""
    return {"status": "online", "message": "Logistics API is ready."}

@app.get("/metrics/top", response_model=List[LocationMetric])
async def get_top_locations(limit: int = Query(10, ge=1, le=100)):
    """
    Get the busiest pickup locations.
    - **limit**: Number of locations to return (1-100).
    """
    conn = await get_db_connection()
    try:
        # Best Practice: Explicitly list columns instead of SELECT *
        query = """
            SELECT location_id, avg_dist, trip_count, avg_cost
            FROM location_metrics 
            ORDER BY trip_count DESC 
            LIMIT $1
        """
        rows = await conn.fetch(query, limit)
        return [dict(row) for row in rows]
    finally:
        await conn.close()

@app.get("/metrics/{location_id}", response_model=LocationMetric)
async def get_location_stats(location_id: int):
    """
    Get stats for a specific specific location ID (e.g., 132 for JFK Airport).
    """
    conn = await get_db_connection()
    try:
        query = """
            SELECT location_id, avg_dist, trip_count, avg_cost
            FROM location_metrics 
            WHERE location_id = $1
        """
        row = await conn.fetchrow(query, location_id)
        
        if row is None:
            raise HTTPException(status_code=404, detail="Location ID not found")
            
        return dict(row)
    finally:
        await conn.close()