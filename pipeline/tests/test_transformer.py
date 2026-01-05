from pipeline.transformer import transform_raw_data

def test_transform_raw_data_success():
    """
    Tests that the transformer function correctly processes a valid raw data object.
    """
    sample_raw_data = {
        "Meta Data": {
            "1. Information": "Daily Prices",
            "2. Symbol": "TEST",
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
            }
        }
    }
    
    result = transform_raw_data(sample_raw_data, "TEST")
    
    # Assert that the transformation was successful and produced one record
    assert len(result) == 1
    
    record = result[0]
    # Assert that the data types are correct after transformation
    assert isinstance(record['open'], float)
    assert isinstance(record['volume'], int)
    # Assert that the new fields were added correctly
    assert record['symbol'] == "TEST"
    assert record['date'] == "2024-01-01"

if __name__ == "__main__":
    test_transform_raw_data_success()
    print("Test passed successfully!")