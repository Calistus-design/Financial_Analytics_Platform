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

export interface MarketOverview {
  total_volume: number;
  top_gainer_symbol: string;
  top_gainer_change: number;
  top_loser_symbol: string;
  top_loser_change: number;
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

export const fetchMarketOverview = async (): Promise<MarketOverview | null> => {
  try {
    const response = await apiClient.get('/api/market-overview');
    return response.data;
  } catch (error) {
    console.error("Error fetching market overview:", error);
    return null;
  }
};