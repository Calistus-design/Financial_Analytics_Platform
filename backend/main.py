"""
Backend API for the Financial Analytics Platform.

This module uses FastAPI to create a web server that serves processed
stock market data from the SQLite database populated by the ETL pipeline.
"""
import os
from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, text
from typing import List
from .models import StockData, MarketOverview
from fastapi.middleware.cors import CORSMiddleware

# Import the Pydantic models we just created
from .models import StockData

# --- 1. SETUP ---
app = FastAPI(
    title="Financial Analytics API",
    description="An API for accessing processed stock market data.",
    version="1.0.0"
)

# --- ADD CORS MIDDLEWARE ---
# Define the list of origins that are allowed to make requests to our API
origins = [
    "http://localhost:3000", # The default port for React's development server
    "http://localhost",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # Allow requests from these specific origins
    allow_credentials=True,      # Allow cookies (not used now, but good practice)
    allow_methods=["*"],         # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],         # Allow all headers
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

# Endpoint that provides high-level summary KPIs
@app.get("/api/market-overview", response_model=MarketOverview)
def get_market_overview():
    """
    Retrieves high-level market KPIs for the most recent day of data.
    Calculates total volume, and identifies the top gainer and loser.
    """
    # Query to find the absolute latest date available in the database
    latest_date_query = "SELECT MAX(date) FROM stock_data"
    
    try:
        with engine.connect() as connection:
            latest_date_result = connection.execute(text(latest_date_query))
            latest_date = latest_date_result.scalar_one_or_none()

        if not latest_date:
            raise HTTPException(status_code=404, detail="No data available to calculate overview.")

        # Query to get all data for that latest date and calculate KPIs
        overview_query = text("""
            WITH latest_day_data AS (
                SELECT
                    *,
                    ((close - open) / open) AS pct_change
                FROM stock_data
                WHERE date = :latest_date
            )
            SELECT
                (SELECT SUM(volume) FROM latest_day_data) AS total_volume,
                (SELECT symbol FROM latest_day_data ORDER BY pct_change DESC LIMIT 1) AS top_gainer_symbol,
                (SELECT MAX(pct_change) FROM latest_day_data) AS top_gainer_change,
                (SELECT symbol FROM latest_day_data ORDER BY pct_change ASC LIMIT 1) AS top_loser_symbol,
                (SELECT MIN(pct_change) FROM latest_day_data) AS top_loser_change;
        """)

        with engine.connect() as connection:
            result = connection.execute(overview_query, {"latest_date": latest_date})
            overview_data = result.mappings().one() # .one() gets a single result

        return overview_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")