import pandas as pd
from sqlalchemy import create_engine

# Connection String (Same as your pipeline)
DB_URL = 'postgresql://user:password@localhost:5432/taxidata'

def check_data():
    engine = create_engine(DB_URL)
    
    # Read the table directly into a DataFrame
    print("Reading from Database...")
    df = pd.read_sql("SELECT * FROM location_metrics LIMIT 5", engine)
    
    print("\n--- DATA FROM POSTGRES ---")
    print(df)

if __name__ == "__main__":
    check_data()