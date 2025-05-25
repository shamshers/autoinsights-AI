import React from 'react';

const EDADisplay = ({ stats }) => {
  if (!stats || typeof stats === 'string') return <p>{stats}</p>;

  return (
    <div>
      <pre>{JSON.stringify(stats, null, 2)}</pre>
    </div>
  );
};

export default EDADisplay;
