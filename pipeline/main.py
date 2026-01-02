"""
Main ETL Pipeline Orchestrator.

This script serves as the main entry point for the entire ETL pipeline.
It orchestrates the process of fetching, transforming, loading and
reporting on stock market data by calling the respective modules in sequence.

This script is intended to be run automatically on a schedule (e.g., via GitHub Actions).
"""
import asyncio
import httpx

# Import the functions from our other pipeline modules
from .api_client import fetch_stock_data
from .transformer import transform_raw_data
from .loader import create_stock_data_table, load_data_to_db
from .reporter import generate_pdf_report

# Define the list of stocks we want to track
STOCKS_TO_TRACK = ["IBM", "AAPL", "GOOG", "MSFT", "NVDA"]

async def run_pipeline():
    """
    Executes the full ETL pipeline for all tracked stocks.
    """
    print("--- Starting ETL Pipeline ---")
    
    # --- EXTRACT ---
    print(f"Fetching data for {len(STOCKS_TO_TRACK)} stocks...")
    all_raw_data = []
    async with httpx.AsyncClient() as client:
        # We will fetch sequentially to respect the API limit, but async client is still good practice
        for symbol in STOCKS_TO_TRACK:
            await asyncio.sleep(15) # Add a 15-second delay to be very safe with the API limit
            raw_data = await fetch_stock_data(client, symbol)
            if raw_data and "Meta Data" in raw_data:
                all_raw_data.append((symbol, raw_data))
            elif raw_data:
                print(f"API returned a note for {symbol}: {raw_data.get('Note', 'No data returned')}")

    if not all_raw_data:
        print("No data fetched. Exiting pipeline.")
        return

    # --- TRANSFORM ---
    print("\nTransforming raw data...")
    all_clean_records = []
    for symbol, raw_data in all_raw_data:
        clean_records = transform_raw_data(raw_data, symbol)
        if clean_records:
            all_clean_records.extend(clean_records)
    
    if not all_clean_records:
        print("No data was successfully transformed. Exiting pipeline.")
        return

    # --- LOAD ---
    print("\nLoading data into database...")
    create_stock_data_table() # Ensure table exists
    load_data_to_db(all_clean_records)

    # --- REPORT ---
    print("\nGenerating daily PDF report...")
    generate_pdf_report(all_clean_records)

    print("\n--- ETL Pipeline Finished Successfully ---")


if __name__ == '__main__':
    # Use asyncio.run() to execute our async main function
    asyncio.run(run_pipeline())