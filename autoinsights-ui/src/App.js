import React, { useState } from 'react';
import UploadForm from './components/UploadForm';
import ResultPanel from './components/ResultPanel';

function App() {
  const [result, setResult] = useState(null);

  return (
    <div className="App">
      <h1>AutoInsights AI</h1>
      <UploadForm onResult={(res) => {
        console.log("📦 API Response:", res);
        setResult(res);
      }} />
      {result && <ResultPanel result={result} />}
    </div>
  );
}

export default App;
