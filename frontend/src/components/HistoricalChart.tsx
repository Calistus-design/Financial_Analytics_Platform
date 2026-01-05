import React from 'react';
import { 
  LineChart, Line, BarChart, Bar, PieChart, Pie, Cell, XAxis, YAxis, 
  CartesianGrid, Tooltip, Legend, ResponsiveContainer 
} from 'recharts';
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
  
  // --- 1. Frontend Data Transformation for Pie Chart ---
  const upDays = data.filter(d => d.close > d.open).length;
  const downDays = data.length - upDays;
  const pieData = [
    { name: 'Up Days', value: upDays },
    { name: 'Down Days', value: downDays },
  ];
  const PIE_COLORS = ['#28a745', '#dc3545']; // Green for up, Red for down

  // Format Y-axis ticks for volume to be more readable
  const formatVolume = (tickItem: number) => {
    if (tickItem > 1000000) return `${(tickItem / 1000000).toFixed(1)}M`;
    if (tickItem > 1000) return `${(tickItem / 1000).toFixed(0)}K`;
    return tickItem.toString();
  };

  return (
    <div style={{ marginTop: '40px' }}>
      <h2>Historical Performance for {symbol}</h2>
      {/* We'll adjust the layout to fit three charts */}
      <div style={{ display: 'flex', gap: '20px', width: '100%', height: '400px' }}>
        
        {/* Chart 1: Close Price (Line Chart) */}
        <div style={{ width: '40%', height: '100%' }}>
          <ResponsiveContainer>
            <LineChart data={data}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis domain={['dataMin - 5', 'dataMax + 5']} />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="close" name="Close Price" stroke="#8884d8" dot={false} />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Chart 2: Volume (Bar Chart) */}
        <div style={{ width: '40%', height: '100%' }}>
          <ResponsiveContainer>
            <BarChart data={data}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis tickFormatter={formatVolume} />
              <Tooltip />
              <Legend />
              <Bar dataKey="volume" name="Trading Volume" fill="#82ca9d" />
            </BarChart>
          </ResponsiveContainer>
        </div>
        
        {/* Chart 3: Market Sentiment (Pie Chart) */}
        <div style={{ width: '20%', height: '100%', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
          <h4 style={{ margin: '0 0 10px 0' }}>Daily Sentiment</h4>
          <ResponsiveContainer>
            <PieChart>
              <Pie data={pieData} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={80} label>
                {pieData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={PIE_COLORS[index % PIE_COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </div>

      </div>
    </div>
  );
};