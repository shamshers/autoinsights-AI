import matplotlib.pyplot as plt
import pandas as pd
from app.agents.agent_base import AgentBase

class VisualizationAgent(AgentBase):
    order = 4

    def run(self, state):
        df = state.get("cleaned_df")

        if df is None or df.empty:
            print("[VisualizationAgent] ❌ No DataFrame found in state.")
            state["visualization_status"] = "No data available for charts."
            state["chart_fig"] = None
            return state

        try:
            numeric_columns = df.select_dtypes(include='number').columns.tolist()
            if not numeric_columns:
                print("[VisualizationAgent] ❌ No numeric columns for plotting.")
                state["visualization_status"] = "No numeric data to visualize."
                state["chart_fig"] = None
                return state

            fig, ax = plt.subplots(figsize=(10, 6))
            df[numeric_columns].plot(kind='bar', ax=ax)
            plt.title("Auto Insights - Bar Chart of Numeric Columns")
            plt.tight_layout()

            print("[VisualizationAgent] ✅ Chart created.")
            state["chart_fig"] = fig
            state["visualization_status"] = "Chart generated."
        except Exception as e:
            print(f"[VisualizationAgent] ❌ Plot error: {e}")
            state["visualization_status"] = f"Plotting error: {e}"
            state["chart_fig"] = None

        return state
