"""
Backend API for the Financial Analytics Platform.

This module uses FastAPI to create a web server that serves processed
stock market data from the SQLite database populated by the ETL pipeline.
"""
import os
from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, text
from typing import List

# Import the Pydantic models we just created
from .models import StockData

# --- 1. SETUP ---
app = FastAPI(
    title="Financial Analytics API",
    description="An API for accessing processed stock market data.",
    version="1.0.0"
)

# --- 2. DATABASE CONNECTION ---
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'market_data.db')
DB_URI = f'sqlite:///{DB_PATH}'
engine = create_engine(DB_URI, connect_args={"check_same_thread": False})


# --- 3. API ENDPOINTS --- ... ---

@app.get("/")
def read_root():
    """A simple endpoint to confirm the API is online."""
    return {"status": "ok", "message": "Welcome to the Financial Analytics API!"}


@app.get("/api/all-stocks", response_model=List[StockData])
def get_all_stocks():
    """
    Retrieves the most recent data point for every stock in the database.
    """
    # This SQL query finds the latest date for each symbol and joins it back
    # to get the full row of data for that latest date.
    query = """
    SELECT s1.*
    FROM stock_data s1
    INNER JOIN (
        SELECT symbol, MAX(date) as max_date
        FROM stock_data
        GROUP BY symbol
    ) s2 ON s1.symbol = s2.symbol AND s1.date = s2.max_date;
    """
    
    try:
        with engine.connect() as connection:
            result = connection.execute(text(query))
            rows = result.mappings().all() # .mappings() allows dict-like access

        if not rows:
            raise HTTPException(status_code=404, detail="No stock data found in the database.")

        # Pydantic will automatically validate that the database rows match our StockData model
        return rows
    except Exception as e:
        # A general catch-all for any other database errors
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")


# Endpoint that can return the full 5,000+ data points for a single stock.
@app.get("/api/stock-history/{symbol}", response_model=List[StockData])
def get_stock_history(symbol: str):
    """
    Retrieves the full historical data for a given stock symbol.
    The symbol is passed as a path parameter.
    """
    # Using a parameterized query to prevent SQL injection
    query = text("SELECT * FROM stock_data WHERE symbol = :symbol ORDER BY date ASC")
    
    try:
        with engine.connect() as connection:
            result = connection.execute(query, {"symbol": symbol.upper()})
            rows = result.mappings().all()

        if not rows:
            raise HTTPException(status_code=404, detail=f"No data found for symbol '{symbol}'.")

        return rows
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")