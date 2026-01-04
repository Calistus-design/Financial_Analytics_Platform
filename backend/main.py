"""
Backend API for the Financial Analytics Platform.

This module uses FastAPI to create a web server that serves processed
stock market data from the SQLite database populated by the ETL pipeline.
"""
import os
from fastapi import FastAPI
from sqlalchemy import create_engine, text

# Create a FastAPI app instance
app = FastAPI(
    title="Financial Analytics API",
    description="An API for accessing processed stock market data.",
    version="1.0.0"
)

# Define the path to the database file created by the pipeline
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'market_data.db')
DB_URI = f'sqlite:///{DB_PATH}'

# Create a SQLAlchemy engine
# 'check_same_thread' is a specific requirement for SQLite with FastAPI
engine = create_engine(DB_URI, connect_args={"check_same_thread": False})


# We will define our endpoints here in the upcoming steps.

# Example: A simple root endpoint to confirm the API is running
@app.get("/")
def read_root():
    """A simple endpoint to confirm the API is online."""
    return {"status": "ok", "message": "Welcome to the Financial Analytics API!"}