# app/agents/ingestion_agent.py

import pandas as pd
from app.agents.agent_base import AgentBase
import os

class IngestionAgent(AgentBase):
    order = 1

    def run(self, state):
        print(f"[IngestionAgent] file_path from state: {state.get('file_path')}")
        file_path = state.get("file_path")
        print(f"[IngestionAgent] Received file_path: {file_path}")

        try:
            if not file_path or not os.path.exists(file_path):
                raise FileNotFoundError("file_path is missing or does not exist.")

            if file_path.endswith(".csv"):
                df = pd.read_csv(file_path)
            elif file_path.endswith((".xls", ".xlsx")):
                df = pd.read_excel(file_path)
            else:
                raise ValueError("Unsupported file format")

            if df.empty:
                raise ValueError("Uploaded file contains no data.")

            print(f"[IngestionAgent] Loaded DataFrame with shape: {df.shape}")
            state["raw_df"] = df
        except Exception as e:
            print(f"[IngestionAgent] ❌ Error: {e}")
            state["raw_df"] = None
            state["error"] = f"IngestionAgent error: {e}"

        return state
