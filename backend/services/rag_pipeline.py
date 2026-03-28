"""
RAG Pipeline with Hardware-Aware Personalization.

Processes user queries with hardware context injection for personalized responses.
"""

import logging
import time
from typing import Optional

from sqlalchemy.orm import Session

from services.hardware_context_service import HardwareContextService
from services.performance_monitor import get_performance_monitor
from llm.grok_client import GrokClient
from retrieval.qdrant_service import QdrantService
from config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class RAGPipeline:
    """
    RAG pipeline with hardware-aware personalization.
    
    Retrieves relevant context from Qdrant and generates responses
    using Grok API with hardware-specific constraints.
    """
    
    def __init__(self, db: Optional[Session] = None):
        """
        Initialize RAG pipeline.
        
        Args:
            db: Optional database session for hardware context
        """
        self.db = db
        self.grok_client = GrokClient()
        self.qdrant_service = QdrantService()
        self.hardware_context_service = HardwareContextService(db) if db else None
    
    async def process_query(
        self,
        query: str,
        user_id: Optional[str] = None,
        selected_text: Optional[str] = None,
        session_id: Optional[str] = None,
    ) -> dict:
        """
        Process a user query with optional hardware personalization.

        Args:
            query: User's query text
            user_id: Optional user ID for hardware context
            selected_text: Optional text selected by user
            session_id: Optional session ID for conversation tracking

        Returns:
            dict: Response with answer, sources, and metadata
        """
        logger.info(f"Processing query: {query[:100]}...")
        monitor = get_performance_monitor()

        # Step 1: Retrieve relevant context from Qdrant (Search step)
        start_time = time.time()
        retrieved_docs = await self.qdrant_service.search(query, top_k=5)
        search_latency_ms = (time.time() - start_time) * 1000
        monitor.record_step_latency("search", search_latency_ms, "rag_pipeline", user_id)
        logger.debug(f"Search step completed in {search_latency_ms:.2f}ms")

        # Step 2: Build system prompt with hardware context (Context Assembly step)
        start_time = time.time()
        system_prompt = self._build_system_prompt(
            retrieved_docs=retrieved_docs,
            user_id=user_id,
            selected_text=selected_text,
        )
        context_assembly_latency_ms = (time.time() - start_time) * 1000
        monitor.record_step_latency("context_assembly", context_assembly_latency_ms, "rag_pipeline", user_id)
        logger.debug(f"Context assembly step completed in {context_assembly_latency_ms:.2f}ms")

        # Step 3: Generate response with Grok (LLM Call step)
        start_time = time.time()
        response_text = await self.grok_client.generate(
            system_prompt=system_prompt,
            user_query=query,
        )
        llm_call_latency_ms = (time.time() - start_time) * 1000
        monitor.record_step_latency("llm_call", llm_call_latency_ms, "rag_pipeline", user_id)
        logger.debug(f"LLM call step completed in {llm_call_latency_ms:.2f}ms")

        # Step 4: Build response with sources
        response = {
            "response": response_text,
            "sources": self._format_sources(retrieved_docs),
            "confidence": self._calculate_confidence(retrieved_docs),
            "session_id": session_id,
        }

        # Add hardware context metadata if available
        if user_id and self.hardware_context_service:
            hardware_context = self.hardware_context_service.get_user_context(user_id)
            if hardware_context:
                response["hardware_context_used"] = True
                response["hardware_type"] = hardware_context.get("hardware_type")
                response["pdf_pages_referenced"] = hardware_context.get("pdf_pages", [])

        logger.info(f"Query processed successfully for user {user_id}")
        return response
    
    def _build_system_prompt(
        self,
        retrieved_docs: list,
        user_id: Optional[str] = None,
        selected_text: Optional[str] = None,
    ) -> str:
        """
        Build system prompt with retrieved context and hardware personalization.
        
        Args:
            retrieved_docs: Retrieved documents from Qdrant
            user_id: Optional user ID for hardware context
            selected_text: Optional selected text
            
        Returns:
            str: Formatted system prompt
        """
        # Base system prompt
        system_prompt = """You are a Physical AI textbook assistant.
Your role is to help students learn about Physical AI, ROS 2, Gazebo, NVIDIA Isaac, and humanoid robotics.

Guidelines:
- Provide clear, accurate technical information
- Reference textbook content when available
- Adapt your explanations to the student's level
- If unsure, acknowledge limitations"""
        
        # Add selected text context if provided
        if selected_text:
            system_prompt += f"\n\nStudent Selected Text:\n{selected_text}"
        
        # Add retrieved context
        if retrieved_docs:
            context = "\n\nRelevant Textbook Content:\n"
            for i, doc in enumerate(retrieved_docs, 1):
                context += f"\n{i}. {doc.get('content', '')[:500]}...\n"
            system_prompt += context
        
        # Add hardware context if user is authenticated
        if user_id and self.hardware_context_service:
            hardware_prompt = self.hardware_context_service.inject_context(
                system_prompt="",  # Empty because we're building custom prompt
                user_id=user_id,
            )
            
            # Extract just the hardware context part
            if "<Hardware Context>" in hardware_prompt:
                hardware_section = hardware_prompt.split("<Hardware Context>")[1].split("</Hardware Context>")[0]
                system_prompt += f"\n\n<Hardware Context>{hardware_section}</Hardware Context>"
                
                logger.info(f"Hardware context injected for user {user_id}")
        
        return system_prompt
    
    def _format_sources(self, retrieved_docs: list) -> list:
        """
        Format retrieved documents as sources.

        Args:
            retrieved_docs: Retrieved documents

        Returns:
            list: Formatted sources
        """
        sources = []
        for doc in retrieved_docs:
            metadata = doc.get('metadata', {})
            sources.append({
                "file_name": metadata.get('file_name', 'Unknown'),
                "chunk_index": metadata.get('chunk_index', 'Unknown'),
                "uploaded_at": metadata.get('uploaded_at', 'Unknown'),
                "similarity_score": doc.get('score', 0.0),
            })
        return sources
    
    def _calculate_confidence(self, retrieved_docs: list) -> float:
        """
        Calculate confidence score based on retrieved documents.
        
        Args:
            retrieved_docs: Retrieved documents
            
        Returns:
            float: Confidence score (0.0-1.0)
        """
        if not retrieved_docs:
            return 0.0
        
        # Use highest similarity score as confidence
        max_score = max(doc.get('score', 0.0) for doc in retrieved_docs)
        return min(1.0, max_score)
