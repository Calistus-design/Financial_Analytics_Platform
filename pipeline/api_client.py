"""
Asynchronous API Client for Alpha Vantage.

This module is responsible for all communication with the Alpha Vantage API.
It uses an asynchronous approach to fetch data for multiple stock symbols
concurrently, which is significantly faster than fetching them sequentially.
It handles the API key securely and includes robust error handling.

Functions:
    fetch_stock_data(symbol: str) -> dict | None: 
        Fetches daily time series data for a single stock symbol.
"""
import os
import asyncio
import httpx
from dotenv import load_dotenv
from typing import Union

# Load environment variables from .env file
load_dotenv()

API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
BASE_URL = "https://www.alphavantage.co/query"

async def fetch_stock_data(client: httpx.AsyncClient, symbol: str) -> Union[dict, None]:
    """
    Asynchronously fetches daily stock data for a given symbol.
    """
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "apikey": API_KEY,
        "outputsize": "compact"
    }
    
    try:
        response = await client.get(BASE_URL, params=params, timeout=30.0)
        response.raise_for_status()
        print(f"Successfully fetched data for {symbol}")
        return response.json()
    except httpx.HTTPStatusError as http_err:
        print(f"HTTP error occurred for {symbol}: {http_err}")
    except httpx.RequestError as err:
        print(f"An error occurred for {symbol}: {err}")
    
    return None

# Example of how to run this script directly for testing
async def main_test():
    """Main function to test controlled concurrent fetching."""
    # A semaphore to limit concurrent requests to 2 at a time
    semaphore = asyncio.Semaphore(1)

    symbols_to_test = ["IBM", "AAPL", "GOOG", "MSFT"] # Let's add one more

    async def fetch_with_semaphore(client, symbol):
        async with semaphore:
            # Add a small delay to be respectful to the API
            await asyncio.sleep(1) 
            return await fetch_stock_data(client, symbol)

    print("--- Starting Compliant Fetch (1 at a time) ---")
    async with httpx.AsyncClient() as client:
        tasks = [fetch_with_semaphore(client, symbol) for symbol in symbols_to_test]
        results = await asyncio.gather(*tasks)
    
    print("\n--- Fetching Complete ---")
    for symbol, data in zip(symbols_to_test, results):
        if data and "Meta Data" in data:
            print(f"Result for {symbol}: Success (contains '{list(data.keys())[0]}')")
        elif data:
            # This will print the API's note if we get rate-limited
            print(f"Result for {symbol}: API Note/Error - {data}")
        else:
            print(f"Result for {symbol}: Failed to fetch data")


if __name__ == "__main__":
    asyncio.run(main_test())