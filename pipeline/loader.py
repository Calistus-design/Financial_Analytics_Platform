"""
Database Loader Module.

This module is responsible for loading the transformed, clean data into
a persistent storage layer. It uses SQLite as the database and SQLAlchemy
Core for database interactions, ensuring a robust and well-structured
approach to data persistence.
"""
import os
import pandas as pd
from typing import List
from sqlalchemy import create_engine, text

# Define the path for the database relative to the project root
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'market_data.db')
DB_URI = f'sqlite:///{DB_PATH}'

# Ensure the 'data' directory exists
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

# Create a database engine
engine = create_engine(DB_URI)

def create_stock_data_table():
    """Creates the stock_data table if it doesn't already exist."""
    
    # This SQL statement is written to be idempotent (it won't fail if the table already exists)
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS stock_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        symbol TEXT NOT NULL,
        date TEXT NOT NULL,
        open REAL NOT NULL,
        high REAL NOT NULL,
        low REAL NOT NULL,
        close REAL NOT NULL,
        volume INTEGER NOT NULL,
        UNIQUE(symbol, date) -- Ensures we don't insert duplicate data for the same stock on the same day
    );
    """
    try:
        with engine.connect() as connection:
            connection.execute(text(create_table_sql))
        print("Table 'stock_data' is ready.")
    except Exception as e:
        print(f"Error creating table: {e}")


def load_data_to_db(clean_records: List[dict]):
    """
    Loads a list of clean records into the SQLite database.
    
    Uses pandas to facilitate the loading process and handles potential
    integrity errors (like duplicate entries) gracefully.
    """
    if not clean_records:
        print("No records to load.")
        return

    df = pd.DataFrame(clean_records)
    
    # Reorder columns to match the table structure (optional but good practice)
    df = df[['symbol', 'date', 'open', 'high', 'low', 'close', 'volume']]
    
    try:
        # 'to_sql' is a powerful pandas function to write to a SQL database
        # 'if_exists='append'' adds new data
        # 'index=False' prevents pandas from writing its own index column
        # 'method='multi'' can be more efficient for inserting many rows
        df.to_sql(
            'stock_data', 
            con=engine, 
            if_exists='append', 
            index=False, 
            method='multi'
        )
        print(f"Successfully loaded {len(df)} records into the database.")
    except Exception as e:
        # This will often catch IntegrityErrors if we try to insert duplicates
        print(f"Error loading data to database: {e}")


# Example of how to run this script directly for testing
if __name__ == '__main__':
    print("Initializing database and table...")
    create_stock_data_table()
    
    print("\nTesting data load...")
    # Create some sample clean records to test the loader
    sample_records = [
        {'symbol': 'TEST', 'date': '2024-01-01', 'open': 100.0, 'high': 102.5, 'low': 99.5, 'close': 101.5, 'volume': 10000},
        {'symbol': 'TEST', 'date': '2024-01-02', 'open': 101.5, 'high': 103.0, 'low': 101.0, 'close': 102.5, 'volume': 12000},
    ]
    load_data_to_db(sample_records)

    print("\nTesting duplicate data load (should be handled gracefully)...")
    # Attempting to load the same data again
    load_data_to_db(sample_records)