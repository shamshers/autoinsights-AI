import React, { useState } from 'react';
import { analyzeData } from '../api';

const UploadForm = ({ onResult }) => {
  const [file, setFile] = useState(null);
  const [query, setQuery] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append('file', file);
    formData.append('user_query', query);

try {
  const result = await analyzeData(formData);
  onResult(result);
} catch (err) {
  console.error("❌ API Error:", err);
  alert("API call failed. Check backend or CORS.");
}
  };

  return (
    <form onSubmit={handleSubmit}>
      <input type="file" accept=".csv,.xlsx" onChange={(e) => setFile(e.target.files[0])} required />
      <input type="text" value={query} onChange={(e) => setQuery(e.target.value)} placeholder="Ask your business question..." />
      <button type="submit">Analyze</button>
    </form>
  );
};

export default UploadForm;
