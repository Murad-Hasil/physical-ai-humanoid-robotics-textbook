"""
Qdrant vector database service.

Provides vector storage and retrieval for RAG pipeline.
"""

import logging
import uuid
from typing import List, Dict, Any, Optional
from datetime import datetime

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
    PointIdsList,
    Filter,
    FieldCondition,
    MatchValue,
)
from fastembed import TextEmbedding
from config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class QdrantService:
    """
    Service for interacting with Qdrant vector database.
    
    Provides methods for indexing, searching, and deleting vectors.
    Uses fastembed for lightweight local embedding generation.
    """
    
    COLLECTION_NAME = "physical-ai-docusaurus-textbook"
    EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"  # Lightweight, 384 dimensions
    VECTOR_SIZE = 384
    
    def __init__(self):
        """Initialize Qdrant service with client and embedding model."""
        self.client = None
        self.embedding_model = None
        self._initialized = False
        logger.info("QdrantService initialized")
    
    def _ensure_initialized(self):
        """Lazy initialization of Qdrant client and embedding model."""
        if self._initialized:
            return
        
        try:
            # Try cloud Qdrant first, fall back to in-memory on failure
            if settings.qdrant_url and settings.qdrant_api_key:
                try:
                    cloud_client = QdrantClient(
                        url=settings.qdrant_url,
                        api_key=settings.qdrant_api_key,
                        check_compatibility=False,
                    )
                    # Test the connection
                    cloud_client.get_collections()
                    self.client = cloud_client
                    logger.info("QdrantClient connected to cloud")
                except Exception as cloud_err:
                    logger.warning(f"Qdrant cloud unavailable ({cloud_err}), falling back to in-memory storage")
                    self.client = QdrantClient(":memory:")
            else:
                self.client = QdrantClient(":memory:")
                logger.info("QdrantClient using in-memory storage (development mode)")

            # Initialize embedding model
            self.embedding_model = TextEmbedding(model_name=self.EMBEDDING_MODEL)
            logger.info(f"Embedding model loaded: {self.EMBEDDING_MODEL}")

            # Create collection if not exists
            self._create_collection()

            self._initialized = True

        except Exception as e:
            logger.error(f"Failed to initialize QdrantService: {e}")
            raise
    
    def _create_collection(self):
        """Create Qdrant collection if it doesn't exist."""
        try:
            collections = self.client.get_collections().collections
            collection_exists = any(
                c.name == self.COLLECTION_NAME for c in collections
            )
            
            if not collection_exists:
                self.client.create_collection(
                    collection_name=self.COLLECTION_NAME,
                    vectors_config=VectorParams(
                        size=self.VECTOR_SIZE,
                        distance=Distance.COSINE,
                    ),
                )
                logger.info(f"Collection created: {self.COLLECTION_NAME}")
            else:
                logger.info(f"Collection exists: {self.COLLECTION_NAME}")
                
        except Exception as e:
            logger.error(f"Failed to create collection: {e}")
            raise
    
    def _generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for text using fastembed.
        
        Args:
            text: Text to embed
            
        Returns:
            Embedding vector as list of floats
        """
        embeddings = list(self.embedding_model.embed([text]))
        return embeddings[0].tolist()
    
    async def upsert(self, text: str, metadata: Dict[str, Any]) -> uuid.UUID:
        """
        Upsert a vector with metadata.
        
        Args:
            text: Text to embed and store
            metadata: Metadata to store with vector
            
        Returns:
            Point ID
        """
        self._ensure_initialized()
        
        try:
            # Generate embedding
            embedding = self._generate_embedding(text)
            
            # Create point ID
            point_id = uuid.uuid4()
            
            # Create point with metadata
            point = PointStruct(
                id=str(point_id),
                vector=embedding,
                payload={
                    **metadata,
                    "text": text,  # Store original text
                    "created_at": datetime.utcnow().isoformat(),
                }
            )
            
            # Upsert to Qdrant
            self.client.upsert(
                collection_name=self.COLLECTION_NAME,
                points=[point]
            )
            
            logger.info(f"Upserted point {point_id}")
            return point_id
            
        except Exception as e:
            logger.error(f"Failed to upsert point: {e}")
            raise
    
    async def upsert_batch(self, texts: List[str], metadatas: List[Dict[str, Any]]) -> List[uuid.UUID]:
        """
        Upsert multiple vectors with metadata.
        
        Args:
            texts: List of texts to embed and store
            metadatas: List of metadata dicts
            
        Returns:
            List of point IDs
        """
        self._ensure_initialized()
        
        try:
            # Generate embeddings in batch
            embeddings = list(self.embedding_model.embed(texts))
            
            # Create points
            points = []
            point_ids = []
            
            for text, metadata, embedding in zip(texts, metadatas, embeddings):
                point_id = uuid.uuid4()
                point_ids.append(point_id)
                
                points.append(PointStruct(
                    id=str(point_id),
                    vector=embedding.tolist(),
                    payload={
                        **metadata,
                        "text": text,
                        "created_at": datetime.utcnow().isoformat(),
                    }
                ))
            
            # Upsert batch to Qdrant
            self.client.upsert(
                collection_name=self.COLLECTION_NAME,
                points=points
            )
            
            logger.info(f"Upserted {len(points)} points")
            return point_ids
            
        except Exception as e:
            logger.error(f"Failed to upsert batch: {e}")
            raise
    
    async def search(self, query: str, top_k: int = 5, filters: Optional[Dict] = None) -> List[Dict[str, Any]]:
        """
        Search for similar vectors.
        
        Args:
            query: Query text
            top_k: Number of results
            filters: Optional filters (e.g., file_id)
            
        Returns:
            List of results with scores and metadata
        """
        self._ensure_initialized()
        
        try:
            # Generate query embedding
            query_embedding = self._generate_embedding(query)
            
            # Build filter if provided
            qdrant_filter = None
            if filters:
                conditions = []
                for key, value in filters.items():
                    conditions.append(FieldCondition(
                        key=key,
                        match=MatchValue(value=value)
                    ))
                if conditions:
                    qdrant_filter = Filter(must=conditions)
            
            # Search
            results = self.client.search(
                collection_name=self.COLLECTION_NAME,
                query_vector=query_embedding,
                limit=top_k,
                query_filter=qdrant_filter,
            )
            
            # Format results
            formatted_results = []
            for result in results:
                formatted_results.append({
                    "id": result.id,
                    "score": result.score,
                    "text": result.payload.get("text", ""),
                    "metadata": {
                        k: v for k, v in result.payload.items()
                        if k != "text"
                    }
                })
            
            logger.info(f"Search returned {len(formatted_results)} results")
            return formatted_results
            
        except Exception as e:
            logger.error(f"Search failed: {e}")
            return []
    
    async def delete(self, point_id: uuid.UUID) -> bool:
        """
        Delete a vector by ID.
        
        Args:
            point_id: Point ID to delete
            
        Returns:
            True if deleted
        """
        self._ensure_initialized()
        
        try:
            self.client.delete(
                collection_name=self.COLLECTION_NAME,
                points_selector=PointIdsList(
                    points=[str(point_id)]
                )
            )
            
            logger.info(f"Deleted point {point_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to delete point: {e}")
            return False
    
    async def delete_by_file_id(self, file_id: str) -> int:
        """
        Delete all vectors for a file.
        
        Args:
            file_id: File identifier
            
        Returns:
            Number of deleted points
        """
        self._ensure_initialized()
        
        try:
            # Search for all points with this file_id
            results = self.client.scroll(
                collection_name=self.COLLECTION_NAME,
                scroll_filter=Filter(
                    must=[
                        FieldCondition(
                            key="file_id",
                            match=MatchValue(value=file_id)
                        )
                    ]
                ),
                limit=1000,  # Max limit
            )
            
            points, _ = results
            point_ids = [point.id for point in points]
            
            if point_ids:
                self.client.delete(
                    collection_name=self.COLLECTION_NAME,
                    points_selector=PointIdsList(
                        points=point_ids
                    )
                )
                logger.info(f"Deleted {len(point_ids)} points for file {file_id}")
                return len(point_ids)
            
            return 0
            
        except Exception as e:
            logger.error(f"Failed to delete by file_id: {e}")
            return 0
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """
        Get collection statistics.
        
        Returns:
            Dict with collection info
        """
        self._ensure_initialized()
        
        try:
            info = self.client.get_collection(self.COLLECTION_NAME)
            return {
                "collection_name": self.COLLECTION_NAME,
                "vectors_count": info.vectors_count,
                "points_count": info.points_count,
                "status": str(info.status),
            }
        except Exception as e:
            logger.error(f"Failed to get collection stats: {e}")
            return {"error": str(e)}
