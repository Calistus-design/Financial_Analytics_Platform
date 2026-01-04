"""
Pydantic Models for the API Responses.

These models define the structure of the JSON data that will be sent
from the API to the client (e.g., the React frontend). By using these,
FastAPI can provide automatic data validation, serialization, and
documentation for our API.
"""
from pydantic import BaseModel
from datetime import date
from typing import List

class StockData(BaseModel):
    """Defines the structure for a single stock data point in the API response."""
    symbol: str
    date: date
    open: float
    high: float
    low: float
    close: float
    volume: int

    # This config allows the model to be created from database objects
    class Config:
        from_attributes = True

class MarketOverview(BaseModel):
    """Defines the structure for the market overview KPI response."""
    total_volume: int
    top_gainer_symbol: str
    top_gainer_change: float
    top_loser_symbol: str
    top_loser_change: float