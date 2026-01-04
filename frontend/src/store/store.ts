import { create } from 'zustand';

// First, let's define the TypeScript types for our data
// This gives us type safety and autocompletion
export interface StockData {
  symbol: string;
  date: string;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
}

// Now, define the shape of our store's state
interface AppState {
  allStocks: StockData[];
  selectedSymbol: string | null;
  setSelectedSymbol: (symbol: string) => void;
  setAllStocks: (stocks: StockData[]) => void;
}

// Finally, create the store with our state and the functions to update it
export const useAppStore = create<AppState>((set) => ({
  // Initial state
  allStocks: [],
  selectedSymbol: null,

  // Actions (functions that modify the state)
  setSelectedSymbol: (symbol) => set({ selectedSymbol: symbol }),
  setAllStocks: (stocks) => set({ allStocks: stocks }),
}));