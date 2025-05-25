from .agent_base import AgentBase

class RAGRetrieverAgent(AgentBase):
    """
    Agent for retrieval-augmented generation using Qdrant and sentence-transformers.
    Looks up relevant enterprise docs based on user query or EDA summary.
    """
    def run(self, state):
        from app.core.vector_db import VectorDB

        user_query = state.get('user_query')
        stats = state.get('eda_stats')
        question = user_query or (str(stats) if stats else "business data insights")

        vdb = VectorDB()
        results = vdb.search(question, top_k=2)
        context = "\n\n".join(results)
        state['rag_context'] = context if context else "No relevant documents found."
        print("RAGRetrieverAgent: Retrieved context from vector DB.")
        return state
