"""
Data Transformation and Cleaning Module.

This module is responsible for taking the raw JSON data from the API
and transforming it into a clean, structured, and validated format.
It uses the Pydantic models to parse the data and then flattens the
nested structure into a list of records suitable for database insertion
or data analysis.
"""
import pandas as pd
from typing import List
from .models import RawStockData, StockDataPoint

def transform_raw_data(raw_data: dict, symbol: str) -> List[dict]:
    """
    Transforms raw API data into a clean, flat list of dictionary records.

    Args:
        raw_data: The raw JSON dictionary from the Alpha Vantage API.
        symbol: The stock symbol for which the data was fetched.

    Returns:
        A list of dictionaries, where each dictionary represents a clean
        record for a single day's stock data. Returns an empty list if
        the input data is invalid.
    """
    try:
        # 1. Validate the raw data against our Pydantic model
        validated_data = RawStockData.model_validate(raw_data)
        
        # 2. Flatten the nested structure
        time_series = validated_data.time_series_daily
        clean_records = []
        
        for date_str, data_point in time_series.items():
            record = data_point.model_dump()
            record['date'] = date_str  # Ensure date is a string in the final dict
            record['symbol'] = symbol   # Add the symbol to each record
            clean_records.append(record)
            
        print(f"Successfully transformed {len(clean_records)} records for {symbol}")
        return clean_records

    except Exception as e:
        print(f"Error transforming data for {symbol}: {e}")
        return []

# Example of how to use this for testing
if __name__ == '__main__':
    # This is a sample of the raw data structure from the API
    sample_raw_data = {
        "Meta Data": {
            "1. Information": "Daily Prices",
            "2. Symbol": "IBM",
            "3. Last Refreshed": "2024-01-01",
            "4. Output Size": "Compact",
            "5. Time Zone": "US/Eastern"
        },
        "Time Series (Daily)": {
            "2024-01-01": {
                "1. open": "163.1",
                "2. high": "164.2",
                "3. low": "162.8",
                "4. close": "163.5",
                "5. volume": "3000000"
            },
            "2023-12-31": {
                "1. open": "162.5",
                "2. high": "163.0",
                "3. low": "161.9",
                "4. close": "162.8",
                "5. volume": "2500000"
            }
        }
    }
    
    transformed_data = transform_raw_data(sample_raw_data, "IBM")
    
    if transformed_data:
        # Convert to pandas DataFrame for pretty printing
        df = pd.DataFrame(transformed_data)
        print("\n--- Transformed Data ---")
        print(df.head())
        print("\n--- Data Types ---")
        print(df.info())