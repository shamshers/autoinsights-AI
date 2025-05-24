from .agent_base import AgentBase

class RAGRetrieverAgent(AgentBase):
    """
    Agent for retrieval-augmented generation (stub for now).
    """
    def run(self, state):
        state['rag_context'] = "Sample retrieved context from vector DB."
        print("RAGRetrieverAgent: Retrieved context (stub).")
        return state
