import React, { useEffect } from 'react';
import { useAppStore } from '../store/store';
import { fetchAllStocks } from '../services/apiService';

export const StockDataTable = () => {
  const { allStocks, setAllStocks } = useAppStore();

  useEffect(() => {
    const loadData = async () => {
      const data = await fetchAllStocks();
      setAllStocks(data);
    };

    loadData();
  }, []); // The correct, simplest dependency array to run only once.

  return (
    <div>
      <h2>Market Overview</h2>
      <table style={{ width: '100%', borderCollapse: 'collapse' }}>
        <thead>
          <tr style={{ borderBottom: '2px solid black' }}>
            <th style={{ textAlign: 'left', padding: '8px' }}>Symbol</th>
            <th style={{ textAlign: 'left', padding: '8px' }}>Date</th>
            <th style={{ textAlign: 'right', padding: '8px' }}>Open</th>
            <th style={{ textAlign: 'right', padding: '8px' }}>High</th>
            <th style={{ textAlign: 'right', padding: '8px' }}>Low</th>
            <th style={{ textAlign: 'right', padding: '8px' }}>Close</th>
            <th style={{ textAlign: 'right', padding: '8px' }}>Volume</th>
          </tr>
        </thead>
        <tbody>
          {allStocks.map((stock) => (
            <tr key={stock.symbol} style={{ borderBottom: '1px solid #ccc' }}>
              <td style={{ padding: '8px' }}>{stock.symbol}</td>
              <td style={{ padding: '8px' }}>{stock.date}</td>
              <td style={{ textAlign: 'right', padding: '8px' }}>{stock.open.toFixed(2)}</td>
              <td style={{ textAlign: 'right', padding: '8px' }}>{stock.high.toFixed(2)}</td>
              <td style={{ textAlign: 'right', padding: '8px' }}>{stock.low.toFixed(2)}</td>
              <td style={{ textAlign: 'right', padding: '8px' }}>{stock.close.toFixed(2)}</td>
              <td style={{ textAlign: 'right', padding: '8px' }}>{stock.volume.toLocaleString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};