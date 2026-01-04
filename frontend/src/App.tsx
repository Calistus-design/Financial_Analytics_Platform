import React from 'react';
import './App.css';
import { StockDataTable } from './components/StockDataTable';

function App() {
  return (
    <div className="App">
      <h1>Financial Analytics Dashboard</h1>
      <StockDataTable />
    </div>
  );
}

export default App;