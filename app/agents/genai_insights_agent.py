# app/agents/genai_insights_agent.py

from app.agents.agent_base import AgentBase
from app.core.llm_client import ClaudeClient
import pandas as pd

class GenAIInsightsAgent(AgentBase):
    order = 3  # If you're ordering

    def run(self, state):
        print("[GenAIInsightsAgent] Starting...")

        df = state.get("cleaned_df")
        if df is None or df.empty:
            print("[GenAIInsightsAgent] ❗ No cleaned data, using fallback.")
            df = pd.DataFrame({
                "Region": ["North", "South", "East"],
                "Revenue": [1000, 2000, 1500]
            })

        sample_data = df.head(5).to_string(index=False)
        query = state.get("user_query") or "Summarize this data for business insights."

        prompt = (
            f"You are a data analyst. Please provide a concise business summary of the following dataset:\n\n"
            f"{sample_data}\n\n"
            f"User Question: {query}"
        )

        llm = ClaudeClient()
        summary = llm.generate(prompt)

        print(f"[GenAIInsightsAgent] Summary:\n{summary}")
        state["genai_summary"] = summary if summary else "⚠️ No summary generated."

        return state
