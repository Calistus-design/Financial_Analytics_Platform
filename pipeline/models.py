"""
Pydantic Models for Data Validation.

This module defines the data structures for our application.
Pydantic models are used to enforce a strict schema on our data,
ensuring that the data moving through our pipeline is clean,
validated, and has the correct data types.
"""
from datetime import date
from pydantic import BaseModel, Field, validator

class StockDataPoint(BaseModel):
    """Represents a single day's stock data point."""
    date: date
    open: float = Field(..., alias='1. open')
    high: float = Field(..., alias='2. high')
    low: float = Field(..., alias='3. low')
    close: float = Field(..., alias='4. close')
    volume: int = Field(..., alias='5. volume')

class StockMetaData(BaseModel):
    """Represents the metadata for a stock symbol."""
    information: str = Field(..., alias='1. Information')
    symbol: str = Field(..., alias='2. Symbol')
    last_refreshed: date = Field(..., alias='3. Last Refreshed')
    output_size: str = Field(..., alias='4. Output Size')
    time_zone: str = Field(..., alias='5. Time Zone')

class RawStockData(BaseModel):
    """Represents the raw, nested data structure from the Alpha Vantage API."""
    meta_data: StockMetaData = Field(..., alias='Meta Data')
    time_series_daily: dict[str, StockDataPoint] = Field(..., alias='Time Series (Daily)')