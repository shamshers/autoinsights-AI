# app/agents/test_pipeline.py

from .orchestrator import OrchestratorAgent
from .ingestion_agent import IngestionAgent

def main():
    # Path to a sample CSV or Excel file
    file_path = '../data/sample_datasets/sample.csv'   # <-- update as needed!

    pipeline = OrchestratorAgent([IngestionAgent()])
    init_state = {'file_path': file_path}
    result = pipeline.run(init_state)

    if 'error' in result:
        print("Pipeline error:", result['error'])
    else:
        print("Ingestion Status:", result.get('ingestion_status'))
        print("DataFrame Head:")
        print(result['data'].head())

if __name__ == "__main__":
    main()
