// frontend/src/services/apiService.ts
import axios from 'axios';

// This interface MUST be exported.
export interface StockData {
  symbol: string;
  date: string;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
}

const API_BASE_URL = 'http://127.0.0.1:8000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
});

export const fetchAllStocks = async (): Promise<StockData[]> => {
  try {
    const response = await apiClient.get('/api/all-stocks');
    return response.data;
  } catch (error) {
    console.error("Error fetching all stocks:", error);
    return []; 
  }
};

export const fetchStockHistory = async (symbol: string): Promise<StockData[]> => {
  try {
    const response = await apiClient.get(`/api/stock-history/${symbol}`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching history for ${symbol}:`, error);
    return [];
  }
};