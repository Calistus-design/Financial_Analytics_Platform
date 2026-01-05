// frontend/src/App.tsx
import React, { useState, useEffect } from 'react';
import './App.css';
import { StockDataTable } from './components/StockDataTable';
import { HistoricalChart } from './components/HistoricalChart';
import { fetchAllStocks, fetchStockHistory } from './services/apiService';
import { StockData } from './services/apiService';

function App() {
  // State is now managed here, in the parent component
  const [allStocks, setAllStocks] = useState<StockData[]>([]);
  const [selectedSymbol, setSelectedSymbol] = useState<string | null>(null);
  const [historicalData, setHistoricalData] = useState<StockData[]>([]);

  // Effect to fetch all stocks when the app loads
  useEffect(() => {
    (async () => {
      console.log("APP: Fetching all stocks...");
      const data = await fetchAllStocks();
      setAllStocks(data);
      console.log("APP: All stocks data loaded.");
    })();
  }, []); // Empty array means this runs only once on mount

  // Effect to fetch historical data WHENEVER selectedSymbol changes
  useEffect(() => {
    if (selectedSymbol) {
      (async () => {
        console.log(`APP: Selected symbol changed to ${selectedSymbol}, fetching history...`);
        const data = await fetchStockHistory(selectedSymbol);
        setHistoricalData(data);
        console.log(`APP: History for ${selectedSymbol} loaded.`);
      })();
    }
  }, [selectedSymbol]); // This runs every time selectedSymbol is updated

  return (
    <div className="App">
      <h1>Financial Analytics Dashboard</h1>
      <StockDataTable 
        stocks={allStocks} 
        onRowClick={setSelectedSymbol} 
      />
      <HistoricalChart 
        symbol={selectedSymbol}
        data={historicalData}
      />
    </div>
  );
}

export default App;