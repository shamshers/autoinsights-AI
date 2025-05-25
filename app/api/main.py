import sys

from fastapi import FastAPI

from app.agents.orchestrator import OrchestratorAgent
from app.agents.ingestion_agent import IngestionAgent
from app.agents.cleaning_agent import CleaningAgent
from app.agents.data_science_agent import DataScienceAgent
from app.agents.visualization_agent import VisualizationAgent
from app.agents.genai_insights_agent import GenAIInsightsAgent
from app.agents.rag_retriever_agent import RAGRetrieverAgent
from app.api.routes import router

app = FastAPI(
    title="AutoInsights AI API",
    description="Enterprise Data Analytics API with GenAI & Multi-Agent Pipeline",
    version="1.0.0"
)
app.include_router(router, prefix="/api")
def main(file_path: str, user_query: str = None):
    pipeline = OrchestratorAgent([
        IngestionAgent(),
        CleaningAgent(),
        DataScienceAgent(),
        VisualizationAgent(),
        GenAIInsightsAgent(),
        RAGRetrieverAgent(),
    ])
    state = {
        "file_path": file_path
    }
    if user_query:
        state["user_query"] = user_query

    result = pipeline.run(state)
    print("\n==== PIPELINE RESULTS ====")
    for k, v in result.items():
        if k == 'data':
            print(f"{k}: DataFrame of shape {v.shape}")
        elif k == 'eda_stats':
            print(f"{k}: (truncated) {str(v)[:200]} ...")
        else:
            print(f"{k}: {v}")

    if result.get('error'):
        print("\nERROR:", result['error'])

if __name__ == "__main__":
    # Allow command-line usage:
    # python -m app.agents.main <file_path> [user_query]
    if len(sys.argv) < 2:
        print("Usage: python -m app.agents.main <csv_or_excel_file_path> [user_query]")
        sys.exit(1)
    file_path = sys.argv[1]
    user_query = sys.argv[2] if len(sys.argv) > 2 else None
    main(file_path, user_query)
