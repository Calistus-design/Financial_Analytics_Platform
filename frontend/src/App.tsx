import React, { useState, useEffect } from 'react';
import './App.css';
import { StockDataTable } from './components/StockDataTable';
import { HistoricalChart } from './components/HistoricalChart';
import { KpiCard } from './components/KpiCards';
import { fetchAllStocks, fetchStockHistory, fetchMarketOverview, StockData, MarketOverview } from './services/apiService';

function App() {
  const [allStocks, setAllStocks] = useState<StockData[]>([]);
  const [selectedSymbol, setSelectedSymbol] = useState<string | null>(null);
  const [historicalData, setHistoricalData] = useState<StockData[]>([]);
  const [marketOverview, setMarketOverview] = useState<MarketOverview | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true); // <-- 1. Add loading state

  useEffect(() => {
    (async () => {
      setIsLoading(true); // <-- 2. Set loading to true before fetching
      const [stocksData, overviewData] = await Promise.all([
        fetchAllStocks(),
        fetchMarketOverview()
      ]);
      setAllStocks(stocksData);
      setMarketOverview(overviewData);
      setIsLoading(false); // <-- 3. Set loading to false after fetching
    })();
  }, []);

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

      {/* <-- 4. Main content conditional rendering --> */}
      {isLoading ? (
        <div className="loading-indicator">Loading Dashboard Data...</div>
      ) : (
        <>
          <div style={{ display: 'flex', gap: '20px', marginBottom: '30px' }}>
            {marketOverview && (
              <>
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
              </>
            )}
          </div>

          <StockDataTable 
            stocks={allStocks} 
            onRowClick={setSelectedSymbol} 
          />
          <HistoricalChart 
            symbol={selectedSymbol}
            data={historicalData}
          />
        </>
      )}
    </div>
  );
}

export default App;