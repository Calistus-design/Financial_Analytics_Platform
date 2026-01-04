import axios from 'axios';
import { StockData } from '../store/store'; // Import the type we already defined

// The base URL of our FastAPI backend
const API_BASE_URL = 'http://127.0.0.1:8000';

/**
 * Creates a pre-configured Axios instance.
 * This is a good practice for setting base URLs, headers, etc.
 */
const apiClient = axios.create({
  baseURL: API_BASE_URL,
});

/**
 * Fetches the latest data for all stocks.
 * @returns A promise that resolves to an array of StockData.
 */
export const fetchAllStocks = async (): Promise<StockData[]> => {
  console.log("STEP 1: `fetchAllStocks` function in apiService was called.");
  try {
    console.log("STEP 2: Attempting to make axios request to /api/all-stocks...");
    const response = await apiClient.get('/api/all-stocks');
    console.log("STEP 4: Axios request was successful. Response data:", response.data);
    return response.data;
  } catch (error) {
    console.error("STEP 4 (FAILURE): Axios request failed. Error:", error);
    return []; 
  }
};

/**
 * Fetches the full historical data for a single stock symbol.
 * @param symbol The stock symbol to fetch history for.
 * @returns A promise that resolves to an array of StockData.
 */
export const fetchStockHistory = async (symbol: string): Promise<StockData[]> => {
  try {
    const response = await apiClient.get(`/api/stock-history/${symbol}`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching history for ${symbol}:`, error);
    return [];
  }
};

export {};