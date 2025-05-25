import os
from app.core.vector_db import VectorDB

def ingest_docs(folder="data/docs/"):
    vdb = VectorDB()
    doc_id = 1
    for fname in os.listdir(folder):
        fpath = os.path.join(folder, fname)
        if os.path.isfile(fpath) and fname.endswith('.txt'):
            with open(fpath, 'r', encoding='utf-8') as f:
                text = f.read()
                vdb.add_document(doc_id, text)
                print(f"Ingested: {fname}")
                doc_id += 1

if __name__ == "__main__":
    ingest_docs()
