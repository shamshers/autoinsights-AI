from app.agents.orchestrator import OrchestratorAgent
from app.agents.ingestion_agent import IngestionAgent
from app.agents.cleaning_agent import CleaningAgent
from app.agents.data_science_agent import DataScienceAgent
from app.agents.visualization_agent import VisualizationAgent
from app.agents.genai_insights_agent import GenAIInsightsAgent
from app.agents.rag_retriever_agent import RAGRetrieverAgent

def main():
    file_path = "data/sample_datasets/sample.csv"
    pipeline = OrchestratorAgent([
        IngestionAgent(),
        CleaningAgent(),
        DataScienceAgent(),
        VisualizationAgent(),
        GenAIInsightsAgent(),
        RAGRetrieverAgent(),
    ])
    init_state = {'file_path': file_path}
    result = pipeline.run(init_state)
    print("\n=== Final Pipeline State ===")
    for k, v in result.items():
        if k == 'data':
            print(f"{k}: DataFrame of shape {v.shape}")
        elif k == 'eda_stats':
            print(f"{k}: {str(v)[:80]}...")
        else:
            print(f"{k}: {v}")

if __name__ == "__main__":
    main()
