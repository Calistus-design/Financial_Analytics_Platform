import React from 'react';
import { StockData } from '../services/apiService';

interface StockDataTableProps {
  stocks: StockData[];
  onRowClick: (symbol: string) => void;
}

export const StockDataTable = ({ stocks, onRowClick }: StockDataTableProps) => {
  return (
    <div style={{ marginTop: '20px' }}>
      <h2>Market Overview</h2>
      <table className="stock-table">
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
          {stocks.map((stock) => (
            <tr 
              key={stock.symbol} 
              onClick={() => onRowClick(stock.symbol)}
              style={{ cursor: 'pointer' }}
              onMouseOver={(e) => e.currentTarget.style.backgroundColor = '#f0f0f0'}
              onMouseOut={(e) => e.currentTarget.style.backgroundColor = 'transparent'}
            >
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