from qdrant_client import QdrantClient, models
from sentence_transformers import SentenceTransformer
import os

class VectorDB:
    def __init__(self, host='localhost', port=6333, collection_name="enterprise_docs"):
        self.client = QdrantClient(host=host, port=port)
        self.collection = collection_name
        self.embedder = SentenceTransformer("all-MiniLM-L6-v2")
        # Ensure collection exists
        if self.collection not in [c.name for c in self.client.get_collections().collections]:
            self.client.recreate_collection(
                collection_name=self.collection,
                vectors_config=models.VectorParams(size=384, distance=models.Distance.COSINE),
            )

    def add_document(self, doc_id, text):
        vector = self.embedder.encode(text).tolist()
        self.client.upsert(
            collection_name=self.collection,
            points=[models.PointStruct(id=doc_id, vector=vector, payload={"text": text})],
        )

    def search(self, query, top_k=2):
        query_vector = self.embedder.encode(query).tolist()
        search_result = self.client.search(
            collection_name=self.collection,
            query_vector=query_vector,
            limit=top_k,
        )
        return [hit.payload["text"] for hit in search_result]
