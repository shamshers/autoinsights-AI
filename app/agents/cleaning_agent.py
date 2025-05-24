from .agent_base import AgentBase

class CleaningAgent(AgentBase):
    """
    Enterprise-grade agent for data cleaning.
    Handles missing values and duplicate rows.
    """
    def run(self, state):
        import pandas as pd
        df = state.get('data')
        if df is None or not isinstance(df, pd.DataFrame):
            raise ValueError("CleaningAgent: No DataFrame found in state.")

        original_shape = df.shape

        # Remove duplicates
        df = df.drop_duplicates()

        # Fill missing values (for demo, fill numeric with 0, categorical with 'unknown')
        for col in df.columns:
            if df[col].dtype.kind in 'biufc':
                df[col].fillna(0, inplace=True)
            else:
                df[col].fillna('unknown', inplace=True)

        state['data'] = df
        state['cleaning_status'] = 'success'
        print(f"CleaningAgent: Cleaned data ({original_shape} -> {df.shape}), missing values handled.")
        return state
