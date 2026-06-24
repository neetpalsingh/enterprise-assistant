import chromadb
from chromadb.config import Settings
from typing import List, Dict, Optional
import logging
from openai import OpenAI
import os

logger = logging.getLogger(__name__)

class VectorStore:
    def __init__(self):
        self.client = chromadb.PersistentClient(
            path="./chroma_db",
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )

        self.collection_name = "enterprise_documents"
        self.collection = self._get_or_create_collection()

        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY environment variable is required for RAG functionality. "
                "Please set it in your .env file or environment."
            )
        self.openai_client = OpenAI(api_key=api_key)
    
    def _get_or_create_collection(self):
        try:
            return self.client.get_collection(name=self.collection_name)
        except:
            return self.client.create_collection(
                name=self.collection_name,
                metadata={"description": "Enterprise knowledge base documents"}
            )
    
    def _get_embeddings(self, texts: List[str]) -> List[List[float]]:
        response = self.openai_client.embeddings.create(
            input=texts,
            model="text-embedding-3-small"
        )
        return [item.embedding for item in response.data]
    
    def add_document(
        self,
        document_id: str,
        chunks: List[str],
        metadata: Dict,
        document_type: str = "basic"
    ):
        try:
            embeddings = self._get_embeddings(chunks)
            
            chunk_ids = [f"{document_id}_chunk_{i}" for i in range(len(chunks))]
            
            metadatas = [
                {
                    "document_id": document_id,
                    "file_name": metadata.get("file_name", "unknown"),
                    "document_type": document_type,
                    "chunk_index": i,
                    "total_chunks": len(chunks)
                }
                for i in range(len(chunks))
            ]
            
            self.collection.add(
                ids=chunk_ids,
                embeddings=embeddings,
                documents=chunks,
                metadatas=metadatas
            )
            
            logger.info(f"Added {len(chunks)} chunks for document {document_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error adding document to vector store: {e}")
            raise
    
    def query(
        self,
        query_text: str,
        document_type: Optional[str] = None,
        n_results: int = 5
    ) -> Dict:
        try:
            query_embedding = self._get_embeddings([query_text])[0]
            
            where_filter = None
            if document_type:
                where_filter = {"document_type": document_type}
            
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results,
                where=where_filter
            )
            
            sources = []
            documents = []
            
            if results['documents'] and results['documents'][0]:
                for i, doc in enumerate(results['documents'][0]):
                    documents.append(doc)
                    if results['metadatas'] and results['metadatas'][0]:
                        metadata = results['metadatas'][0][i]
                        sources.append({
                            "file_name": metadata.get("file_name", "unknown"),
                            "document_type": metadata.get("document_type", "basic"),
                            "chunk_index": metadata.get("chunk_index", 0)
                        })
            
            return {
                "documents": documents,
                "sources": sources,
                "metadatas": results.get('metadatas', [[]])[0] if results.get('metadatas') else []
            }
            
        except Exception as e:
            logger.error(f"Error querying vector store: {e}")
            raise
    
    def delete_document(self, document_id: str):
        try:
            results = self.collection.get(
                where={"document_id": document_id}
            )
            
            if results['ids']:
                self.collection.delete(ids=results['ids'])
                logger.info(f"Deleted {len(results['ids'])} chunks for document {document_id}")
                return len(results['ids'])
            
            return 0
            
        except Exception as e:
            logger.error(f"Error deleting document from vector store: {e}")
            raise
    
    def get_stats(self) -> Dict:
        try:
            count = self.collection.count()
            return {
                "total_chunks": count,
                "collection_name": self.collection_name
            }
        except Exception as e:
            logger.error(f"Error getting stats: {e}")
            return {"total_chunks": 0, "collection_name": self.collection_name}
