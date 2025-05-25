import React from 'react';

const ChartViewer = ({ path }) => {
  if (!path) return <p>No chart available.</p>;
  return <img src={`http://localhost:8000${path}`} alt="Data Chart" style={{ maxWidth: '100%' }} />;
};

export default ChartViewer;
