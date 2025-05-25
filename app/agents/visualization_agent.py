# app/agents/visualization_agent.py

from app.agents.agent_base import AgentBase
import pandas as pd
import matplotlib.pyplot as plt
import os
import uuid

class VisualizationAgent(AgentBase):
    order = 4

    def run(self, state):
        df = state.get("cleaned_df")

        if df is None or df.empty:
            print("[VisualizationAgent] ❌ No DataFrame found in state.")
            state["visualization_status"] = "No data available for charts."
            state["chart_path"] = None
            return state

        try:
            numeric_columns = df.select_dtypes(include='number').columns.tolist()

            if not numeric_columns:
                print("[VisualizationAgent] ❌ No numeric columns for plotting.")
                state["visualization_status"] = "No numeric data to visualize."
                return state

            plt.figure(figsize=(10, 6))
            df[numeric_columns].plot(kind='bar')
            plt.title("Auto Insights - Bar Chart of Numeric Columns")
            plt.tight_layout()

            output_dir = "outputs/charts"
            os.makedirs(output_dir, exist_ok=True)
            chart_file = os.path.join(output_dir, f"chart_{uuid.uuid4().hex[:6]}.png")

            plt.savefig(chart_file)
            plt.close()

            print(f"[VisualizationAgent] ✅ Chart saved to: {chart_file}")
            state["chart_path"] = chart_file
            state["visualization_status"] = "Chart generated."
        except Exception as e:
            print(f"[VisualizationAgent] ❌ Plot error: {e}")
            state["visualization_status"] = f"Plotting error: {e}"
            state["chart_path"] = None

        return state
