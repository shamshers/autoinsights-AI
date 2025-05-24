# app/agents/ingestion_agent.py

import pandas as pd
from typing import Dict
from app.agents.agent_base import  AgentBase
import os

class IngestionAgent(AgentBase):
    """
    Enterprise-grade agent for robust data ingestion.
    Supports CSV, Excel; handles errors and schema validation.
    """
    SUPPORTED_FORMATS = ['.csv', '.xlsx', '.xls']

    def run(self, state):
        file_path = state.get('file_path')
        if not file_path:
            raise ValueError("IngestionAgent: No file_path provided in state.")

        ext = os.path.splitext(file_path)[-1].lower()
        if ext not in self.SUPPORTED_FORMATS:
            raise ValueError(f"IngestionAgent: Unsupported file type: {ext}")

        try:
            if ext == '.csv':
                df = pd.read_csv(file_path)
            else:
                df = pd.read_excel(file_path)
        except Exception as e:
            raise RuntimeError(f"IngestionAgent: Error reading file: {e}")

        if df.empty:
            raise ValueError("IngestionAgent: Loaded DataFrame is empty.")

        # Basic schema check (must have at least 2 columns)
        if df.shape[1] < 2:
            raise ValueError("IngestionAgent: Data must have at least 2 columns.")

        state['data'] = df
        state['ingestion_status'] = 'success'
        state['columns'] = list(df.columns)
        print(f"IngestionAgent: Ingested {df.shape[0]} rows, columns: {df.columns.tolist()}")
        return state
