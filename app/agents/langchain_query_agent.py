# app/agents/langchain_query_agent.py

from app.agents.agent_base import AgentBase
import  pandas as pd
import os
from langchain.llms import Claude
from langchain.agents.agent_toolkits import create_pandas_dataframe_agent

class LangChainQueryAgent(AgentBase):
    order = 6  # place after VisualizationAgent

    def run(self, state):
        df = state.get("cleaned_df")
        query = state.get("user_query")

        if df is None or df.empty or not query:
            print("[LangChainQueryAgent] ❌ Missing data or query")
            state["langchain_response"] = "No data or question provided."
            return state

        try:
            llm = Claude(
                temperature=0.0,
                openai_api_key=os.getenv("ANTHROPIC_API_KEY"),
                model_name="claude-3-opus-20240229"
            )

            agent_executor = create_pandas_dataframe_agent(llm, df, verbose=True)
            result = agent_executor.run(query)

            print(f"[LangChainQueryAgent] ✅ Result: {result}")
            state["langchain_response"] = result

        except Exception as e:
            print(f"[LangChainQueryAgent] ❌ Error: {str(e)}")
            state["langchain_response"] = f"Error answering your question: {str(e)}"

        return state
