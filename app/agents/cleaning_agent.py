# app/agents/cleaning_agent.py

from app.agents.agent_base import AgentBase
import pandas as pd

class CleaningAgent(AgentBase):
    order = 2

    def run(self, state):
        df = state.get("raw_df")

        if df is None:
            print("[CleaningAgent] ❌ No raw_df found in state.")
            state["cleaned_df"] = None
            return state

        print(f"[CleaningAgent] ✅ Received raw_df with shape: {df.shape}")

        try:
            df.columns = df.columns.str.strip()
            df.dropna(how='all', inplace=True)

            if df.empty:
                print("[CleaningAgent] ❌ DataFrame is empty after cleaning.")
                state["cleaned_df"] = None
            else:
                print(f"[CleaningAgent] ✅ Cleaned DataFrame shape: {df.shape}")
                state["cleaned_df"] = df

        except Exception as e:
            print(f"[CleaningAgent] ❌ Cleaning error: {e}")
            state["cleaned_df"] = None
            state["error"] = f"CleaningAgent error: {str(e)}"

        return state
