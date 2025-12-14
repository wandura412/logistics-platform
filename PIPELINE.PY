import duckdb
import pandas as pd
from sqlalchemy import create_engine
import time

# --- CONFIGURATION ---
INPUT_FILE = 'yellow_tripdata_2025-01.parquet'
# Connection string: postgresql://user:password@host:port/database
DB_URL = 'postgresql://user:password@localhost:5432/taxidata'

def run_pipeline():
    print("🚀 Starting ETL Pipeline...")
    
    # 1. EXTRACT & TRANSFORM (using DuckDB)
    # We use DuckDB to aggregate millions of rows in seconds.
    print(f"   -> Processing {INPUT_FILE} with DuckDB...")
    
    query = f"""
        SELECT 
            PULocationID as location_id,
            AVG(trip_distance) AS avg_dist,
            COUNT(*) AS trip_count,
            AVG(total_amount) as avg_cost
        FROM '{INPUT_FILE}'
        WHERE passenger_count > 0 
          AND trip_distance > 0
        GROUP BY PULocationID
        HAVING trip_count > 100
        ORDER BY trip_count DESC
    """
    
    # Execute query and get result as a Pandas DataFrame
    con = duckdb.connect()
    metrics_df = con.execute(query).df()
    print(f"   -> Processed. Generated {len(metrics_df)} rows of metrics.")

    # 2. LOAD (using SQLAlchemy)
    print("   -> Loading data into PostgreSQL...")
    engine = create_engine(DB_URL)
    
    # 'replace' drops the table if it exists and creates a new one
    metrics_df.to_sql(name='location_metrics', con=engine, if_exists='replace', index=False)
    
    print("✅ Pipeline Finished! Data is live in the DB.")

if __name__ == "__main__":
    run_pipeline()