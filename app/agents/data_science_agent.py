# app/agents/data_science_agent.py

from app.agents.agent_base import AgentBase

class DataScienceAgent(AgentBase):
    order = 3

    def run(self, state):
        df = state.get("cleaned_df")

        if df is None or df.empty:
            print("[DataScienceAgent] ❌ No DataFrame found in state.")
            state["eda_stats"] = "No data to analyze."
            return state

        # Simple stats for example
        try:
            state["eda_stats"] = df.describe(include='all').to_dict()
            print("[DataScienceAgent] ✅ EDA stats generated.")
        except Exception as e:
            print(f"[DataScienceAgent] ❌ EDA error: {e}")
            state["eda_stats"] = f"EDA error: {str(e)}"

        return state
