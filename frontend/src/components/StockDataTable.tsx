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
      {/* We are back to using the 'stock-table' className from App.css */}
      <table className="stock-table">
        <thead>
          <tr>
            <th>Symbol</th>
            <th>Date</th>
            <th style={{ textAlign: 'right' }}>Open</th>
            <th style={{ textAlign: 'right' }}>High</th>
            <th style={{ textAlign: 'right' }}>Low</th>
            <th style={{ textAlign: 'right' }}>Close</th>
            <th style={{ textAlign: 'right' }}>Volume</th>
          </tr>
        </thead>
        <tbody>
          {stocks.map((stock) => (
            <tr 
              key={stock.symbol} 
              onClick={() => onRowClick(stock.symbol)}
              style={{ cursor: 'pointer' }}
            >
              <td>{stock.symbol}</td>
              <td>{stock.date}</td>
              <td style={{ textAlign: 'right' }}>{stock.open.toFixed(2)}</td>
              <td style={{ textAlign: 'right' }}>{stock.high.toFixed(2)}</td>
              <td style={{ textAlign: 'right' }}>{stock.low.toFixed(2)}</td>
              <td style={{ textAlign: 'right' }}>{stock.close.toFixed(2)}</td>
              <td style={{ textAlign: 'right' }}>{stock.volume.toLocaleString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};