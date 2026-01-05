import React from 'react';

interface KpiCardProps {
  title: string;
  value: string | number;
  color?: string; // Optional color for the value
}

export const KpiCard = ({ title, value, color }: KpiCardProps) => {
  const cardStyle: React.CSSProperties = {
    border: '1px solid #ddd',
    borderRadius: '8px',
    padding: '20px',
    textAlign: 'center',
    boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
    flex: 1, // Allows the cards to grow and fill the space
    minWidth: '150px'
  };

  const titleStyle: React.CSSProperties = {
    margin: 0,
    color: '#666',
    fontSize: '1em'
  };

  const valueStyle: React.CSSProperties = {
    margin: '10px 0 0 0',
    fontSize: '2em',
    fontWeight: 'bold',
    color: color || '#333' // Use the passed color, or default to dark grey
  };

  return (
    <div style={cardStyle}>
      <h3 style={titleStyle}>{title}</h3>
      <p style={valueStyle}>{value}</p>
    </div>
  );
};