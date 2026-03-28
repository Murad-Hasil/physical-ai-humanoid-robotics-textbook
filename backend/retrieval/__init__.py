"""
Retrieval module for vector search.

Exports Qdrant service for RAG pipeline.
"""

from retrieval.qdrant_service import QdrantService

__all__ = ["QdrantService"]
