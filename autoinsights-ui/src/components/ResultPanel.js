import React from 'react';
import ChartViewer from './ChartViewer';
import EDADisplay from './EDADisplay';

const ResultPanel = ({ result }) => (
  <div>
    <h3>Analysis ID: {result.analysis_id}</h3>

    <h4>AI Summary</h4>
    <p>{result.genai_summary}</p>

    <h4>LangChain Answer</h4>
    <p>{result.langchain_response}</p>

    <h4>EDA Statistics</h4>
    <EDADisplay stats={result.eda_stats} />

    <h4>Chart</h4>
    <ChartViewer path={result.chart_path} />
  </div>
);

export default ResultPanel;
