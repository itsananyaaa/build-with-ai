import chromadb
from typing import List, Dict, Any, Optional
from app.models.schemas import MemoryRecord
from app.core.config import settings
from datetime import datetime
import uuid

# Attempt to load SentenceTransformer safely. If the user hasn't run pip install yet, 
# we can wrap it or have it load lazily.
import logging
logger = logging.getLogger(__name__)

class MemorySystem:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MemorySystem, cls).__new__(cls)
            cls._instance.init_system()
        return cls._instance

    def init_system(self):
        self.chroma_client = chromadb.PersistentClient(path=settings.CHROMA_DB_DIR)
        try:
            from sentence_transformers import SentenceTransformer
            self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        except ImportError:
            self.embedder = None
            logger.warning("sentence_transformers not installed, using mock embedder.")

        self.domains = ["student_memory", "business_memory", "fitness_memory", "personal_memory"]
        self.collections = {}
        for domain in self.domains:
            self.collections[domain] = self.chroma_client.get_or_create_collection(name=domain)

    def _get_embedding(self, text: str) -> List[float]:
        if self.embedder:
            return self.embedder.encode(text).tolist()
        return [0.0] * 384 # mock 384-dimensional vector

    def add_memory(self, user_id: str, persona: str, content: str) -> str:
        domain = f"{persona.lower()}_memory"
        if domain not in self.collections:
            domain = "personal_memory"

        collection = self.collections[domain]
        mem_id = str(uuid.uuid4())
        
        # We must insert embedding, document, and metadata
        timestamp = datetime.utcnow().isoformat()
        metadata = {
            "user_id": user_id,
            "persona": persona,
            "timestamp": timestamp
        }
        
        # Insert
        collection.add(
            ids=[mem_id],
            embeddings=[self._get_embedding(content)],
            documents=[content],
            metadatas=[metadata]
        )
        return mem_id

    def search_memory(self, user_id: str, active_persona: str, query: str, limit: int = 5) -> List[MemoryRecord]:
        domain = f"{active_persona.lower()}_memory"
        if domain not in self.collections:
            return []

        collection = self.collections[domain]
        query_embedding = self._get_embedding(query)

        # Retrieve only within active persona unless explicitly allowed 
        # (This implements strict data isolation between personas and users)
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=limit,
            where={"user_id": user_id}
        )

        records: List[MemoryRecord] = []
        if not results['documents']:
            return records

        # We receive a list of lists for each result key
        for doc_list, meta_list in zip(results['documents'], results['metadatas']):
            for doc, meta in zip(doc_list, meta_list):
                records.append(MemoryRecord(
                    user_id=meta['user_id'],
                    persona=meta['persona'],
                    content=doc,
                    timestamp=meta['timestamp']
                ))
        return records

memory_system = MemorySystem()
