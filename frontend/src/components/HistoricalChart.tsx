// frontend/src/components/HistoricalChart.tsx
import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { StockData } from '../services/apiService';

interface HistoricalChartProps {
  symbol: string | null;
  data: StockData[];
}

export const HistoricalChart = ({ symbol, data }: HistoricalChartProps) => {
  if (!symbol) {
    return (
      <div style={{ marginTop: '40px', height: '400px', textAlign: 'center', color: '#888' }}>
        <h2>Click on a stock in the table to see its history.</h2>
      </div>
    );
  }

  return (
    <div style={{ marginTop: '40px', height: '400px' }}>
      <h2>Historical Performance for {symbol}</h2>
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="date" />
          <YAxis domain={['dataMin - 5', 'dataMax + 5']} />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="close" name="Close Price" stroke="#8884d8" activeDot={{ r: 8 }} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};