from .agent_base import AgentBase

class DataScienceAgent(AgentBase):
    """
    Agent for data exploration and (optionally) basic modeling.
    """
    def run(self, state):
        import pandas as pd
        df = state.get('data')
        if df is None or not isinstance(df, pd.DataFrame):
            raise ValueError("DataScienceAgent: No DataFrame found in state.")

        # EDA: summary stats
        stats = df.describe(include='all').to_dict()
        state['eda_stats'] = stats

        # (Optional) Simple model placeholder
        # You can extend this to fit a regression/classification later

        state['data_science_status'] = 'success'
        print("DataScienceAgent: Generated summary statistics.")
        return state
