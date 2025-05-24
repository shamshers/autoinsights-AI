from .agent_base import AgentBase
import pandas as pd
import matplotlib.pyplot as plt

class VisualizationAgent(AgentBase):
    """
    Agent for automated charting (bar chart of first categorical vs first numeric column).
    """
    def run(self, state):


        df = state.get('data')
        if df is None or not isinstance(df, pd.DataFrame):
            raise ValueError("VisualizationAgent: No DataFrame found in state.")

        # Identify columns
        cat_col = None
        num_col = None
        for col in df.columns:
            if pd.api.types.is_numeric_dtype(df[col]) and num_col is None:
                num_col = col
            elif not pd.api.types.is_numeric_dtype(df[col]) and cat_col is None:
                cat_col = col
            if cat_col and num_col:
                break

        if not (cat_col and num_col):
            print("VisualizationAgent: Not enough column types for plotting (need one categorical, one numeric).")
            state['visualization_status'] = 'skipped'
            return state

        # Make bar chart
        plt.figure(figsize=(6, 4))
        try:
            df.groupby(cat_col)[num_col].mean().plot(kind='bar')
            plt.title(f"Average {num_col} by {cat_col}")
            plt.tight_layout()
            chart_path = "data/sample_datasets/auto_chart.png"
            plt.savefig(chart_path)
            plt.close()
            state['chart_path'] = chart_path
            state['visualization_status'] = 'success'
            print(f"VisualizationAgent: Saved bar chart as {chart_path}.")
        except Exception as e:
            print(f"VisualizationAgent: Plotting error: {e}")
            state['visualization_status'] = 'failed'
            state['visualization_error'] = str(e)
        return state
