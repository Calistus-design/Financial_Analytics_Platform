import React, { useState, useEffect } from 'react';
import './App.css';
import { StockDataTable } from './components/StockDataTable';
import { HistoricalChart } from './components/HistoricalChart';
import { KpiCard } from './components/KpiCards'; // <-- 1. Import KpiCard
// Import the new MarketOverview type and fetch function
import { fetchAllStocks, fetchStockHistory, fetchMarketOverview, StockData, MarketOverview } from './services/apiService';

function App() {
  const [allStocks, setAllStocks] = useState<StockData[]>([]);
  const [selectedSymbol, setSelectedSymbol] = useState<string | null>(null);
  const [historicalData, setHistoricalData] = useState<StockData[]>([]);
  // <-- 2. Add new state for the overview data
  const [marketOverview, setMarketOverview] = useState<MarketOverview | null>(null);

  // Effect to fetch initial data (all stocks AND market overview)
  useEffect(() => {
    (async () => {
      console.log("APP: Fetching initial data...");
      // Fetch both sets of data concurrently for better performance
      const [stocksData, overviewData] = await Promise.all([
        fetchAllStocks(),
        fetchMarketOverview()
      ]);
      setAllStocks(stocksData);
      setMarketOverview(overviewData);
      console.log("APP: Initial data loaded.");
    })();
  }, []);

  // ... (useEffect for historicalData remains the same) ...
  useEffect(() => {
    if (selectedSymbol) {
      (async () => {
        const data = await fetchStockHistory(selectedSymbol);
        setHistoricalData(data);
      })();
    }
  }, [selectedSymbol]);

 return (
    <div className="App">
      <h1>Financial Analytics Dashboard</h1>

      {/* If the overview data is still loading, show a message and nothing else */}
      {!marketOverview && <p>Loading market overview...</p>}

      {/* ONLY if the overview data exists, render the flex container and the cards */}
      {marketOverview && (
        <div style={{ display: 'flex', gap: '20px', marginBottom: '30px' }}>
          <KpiCard title="Total Volume" value={marketOverview.total_volume.toLocaleString()} />
          <KpiCard 
            title="Top Gainer" 
            value={`${marketOverview.top_gainer_symbol} (${(marketOverview.top_gainer_change * 100).toFixed(2)}%)`}
            color="#28a745"
          />
          <KpiCard 
            title="Top Loser" 
            value={`${marketOverview.top_loser_symbol} (${(marketOverview.top_loser_change * 100).toFixed(2)}%)`}
            color="#dc3545"
          />
        </div>
      )}

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