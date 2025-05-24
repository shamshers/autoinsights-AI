from .agent_base import AgentBase

class GenAIInsightsAgent(AgentBase):
    """
    Agent for LLM-powered natural language insights using Claude.
    """
    def run(self, state):
        from app.core.llm_client import ClaudeClient

        stats = state.get('eda_stats')
        columns = state.get('columns')
        question = state.get('user_query', None)  # Optional: user prompt from UI/API

        if not stats or not columns:
            raise ValueError("GenAIInsightsAgent: Missing EDA stats or columns in state.")

        claude = ClaudeClient()
        summary = claude.generate_summary(stats, columns, business_question=question)
        state['genai_summary'] = summary
        print("GenAIInsightsAgent: Generated AI summary via Claude.")
        return state
