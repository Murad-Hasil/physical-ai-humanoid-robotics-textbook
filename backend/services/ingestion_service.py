"""
Ingestion service for file upload and indexing.

Handles file uploads, content extraction, and RAG pipeline indexing.
"""

import logging
import os
import tempfile
import uuid
from datetime import datetime
from typing import List, Optional, Dict, Any
from fastapi import UploadFile, HTTPException, status
from sqlalchemy.orm import Session
import json
import pdfplumber

from db.session import get_db
from models.ingestion_log import IngestionLog
from models.user import User
from retrieval.qdrant_service import QdrantService
from config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class IngestionService:
    """
    Service for handling file ingestion and indexing.
    
    Processes uploaded files, extracts content, and indexes to Qdrant.
    """
    
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    ALLOWED_MIME_TYPES = {
        'application/pdf': '.pdf',
        'text/markdown': '.md',
        'text/plain': '.txt',
    }
    ALLOWED_EXTENSIONS = {'.pdf', '.md', '.txt'}
    
    def __init__(self, db: Session):
        """
        Initialize ingestion service.
        
        Args:
            db: Database session
        """
        self.db = db
        self.qdrant_service = QdrantService()
    
    async def validate_file(self, file: UploadFile) -> Dict[str, Any]:
        """
        Validate uploaded file.
        
        Args:
            file: Uploaded file
            
        Returns:
            Dict with validation results
            
        Raises:
            HTTPException: If validation fails
        """
        # Read file content
        content = await file.read()
        file_size = len(content)
        
        # Reset file pointer
        await file.seek(0)
        
        # Check size
        if file_size > self.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_413_PAYLOAD_TOO_LARGE,
                detail={
                    "error": "file_too_large",
                    "message": f"File size exceeds {self.MAX_FILE_SIZE // (1024*1024)}MB limit",
                    "details": {
                        "file_size": file_size,
                        "max_size": self.MAX_FILE_SIZE
                    }
                }
            )
        
        # Check extension
        ext = os.path.splitext(file.filename)[1].lower() if file.filename else ''
        if ext not in self.ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                detail={
                    "error": "unsupported_file_type",
                    "message": f"File type '{ext}' not allowed. Only PDF, Markdown, and Text files are accepted.",
                    "details": {
                        "provided_type": ext,
                        "allowed_types": list(self.ALLOWED_EXTENSIONS)
                    }
                }
            )
        
        # Check MIME type
        if file.content_type not in self.ALLOWED_MIME_TYPES:
            logger.warning(f"MIME type mismatch: {file.content_type} for {file.filename}")
        
        # Verify PDF magic bytes
        if ext == '.pdf':
            if not content[:4].startswith(b'%PDF'):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail={
                        "error": "invalid_pdf",
                        "message": "Invalid PDF file (magic bytes mismatch)"
                    }
                )
        
        return {
            "valid": True,
            "file_size": file_size,
            "extension": ext,
            "content_type": file.content_type
        }
    
    async def extract_content(self, file: UploadFile, file_path: str) -> str:
        """
        Extract text content from file.
        
        Args:
            file: Uploaded file
            file_path: Temporary file path
            
        Returns:
            Extracted text content
        """
        ext = os.path.splitext(file.filename)[1].lower() if file.filename else ''
        
        if ext == '.pdf':
            # Use existing PDF processing if available
            # For now, simple text extraction
            return await self._extract_pdf_content(file_path)
        elif ext in ['.md', '.txt']:
            content = await file.read()
            return content.decode('utf-8')
        
        return ""
    
    async def _extract_pdf_content(self, file_path: str) -> str:
        """
        Extract text from PDF file using pdfplumber.
        
        Handles technical tables and code snippets properly.
        
        Args:
            file_path: Path to PDF file
            
        Returns:
            Extracted text
        """
        text_content = []
        
        try:
            with pdfplumber.open(file_path) as pdf:
                logger.info(f"PDF opened: {len(pdf.pages)} pages")
                
                for page_num, page in enumerate(pdf.pages):
                    # Extract text with layout preservation
                    page_text = page.extract_text(
                        layout=True,  # Preserve layout
                        x_tolerance=1.5,  # Character grouping tolerance
                        y_tolerance=3  # Line grouping tolerance
                    )
                    
                    if page_text:
                        text_content.append(f"--- Page {page_num + 1} ---\n")
                        text_content.append(page_text)
                        text_content.append("\n\n")
                    
                    # Extract tables separately for better structure
                    tables = page.extract_tables()
                    if tables:
                        text_content.append(f"--- Tables on Page {page_num + 1} ---\n")
                        for table_idx, table in enumerate(tables):
                            text_content.append(f"[Table {table_idx + 1}]\n")
                            for row in table:
                                if row:
                                    # Clean and format table row
                                    clean_row = [str(cell).strip() if cell else '' for cell in row]
                                    text_content.append(" | ".join(clean_row) + "\n")
                            text_content.append("\n")
            
            return "".join(text_content)
            
        except Exception as e:
            logger.error(f"PDF extraction failed: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "error": "pdf_extraction_failed",
                    "message": f"Failed to extract text from PDF: {str(e)}"
                }
            )
    
    def _chunk_content(self, content: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
        """
        Split content into overlapping chunks.
        
        Args:
            content: Text content
            chunk_size: Characters per chunk
            overlap: Overlap between chunks
            
        Returns:
            List of text chunks
        """
        chunks = []
        start = 0
        content_length = len(content)
        
        while start < content_length:
            end = start + chunk_size
            chunk = content[start:end]
            
            # Try to break at sentence boundary
            if end < content_length:
                last_period = chunk.rfind('.')
                if last_period > chunk_size // 2:
                    chunk = chunk[:last_period + 1]
                    end = start + last_period + 1
            
            chunks.append(chunk.strip())
            start = end - overlap
        
        return chunks
    
    async def process_upload(
        self,
        file: UploadFile,
        user: User,
        temp_dir: Optional[str] = None
    ) -> IngestionLog:
        """
        Process uploaded file and index to Qdrant.
        
        Args:
            file: Uploaded file
            user: Admin user performing upload
            temp_dir: Optional temporary directory
            
        Returns:
            IngestionLog with processing results
        """
        # Validate file
        validation = await self.validate_file(file)
        
        # Create ingestion log
        log = IngestionLog(
            user_id=user.id,
            file_name=file.filename,
            file_path="",
            file_size=validation["file_size"],
            file_type=file.content_type,
            status="processing"
        )
        self.db.add(log)
        self.db.commit()
        self.db.refresh(log)
        
        try:
            # Save to temporary file
            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=validation["extension"],
                dir=temp_dir
            ) as tmp:
                content = await file.read()
                tmp.write(content)
                tmp_path = tmp.name
            
            # Update log with file path
            log.file_path = tmp_path
            self.db.commit()
            
            # Extract content
            content = await self.extract_content(file, tmp_path)
            
            # Chunk content
            chunks = self._chunk_content(content)
            
            # Index to Qdrant
            file_id = str(log.id)
            point_ids = await self._index_to_qdrant(
                chunks=chunks,
                file_id=file_id,
                file_name=file.filename,
                user_id=str(user.id),
                file_type=validation["extension"],
                file_size=validation["file_size"]
            )
            
            # Update log with success
            log.status = "completed"
            log.chunk_count = len(chunks)
            log.qdrant_point_ids = json.dumps([str(pid) for pid in point_ids])
            log.completed_at = datetime.utcnow()
            
            logger.info(f"Successfully indexed {file.filename}: {len(chunks)} chunks")
            
        except Exception as e:
            logger.error(f"Failed to process {file.filename}: {e}")
            log.status = "failed"
            log.error_message = str(e)
            log.completed_at = datetime.utcnow()
            
            # Cleanup temp file
            if hasattr(log, 'file_path') and log.file_path and os.path.exists(log.file_path):
                os.unlink(log.file_path)
        
        finally:
            self.db.commit()
        
        return log
    
    async def _index_to_qdrant(
        self,
        chunks: List[str],
        file_id: str,
        file_name: str,
        user_id: str,
        file_type: str,
        file_size: int
    ) -> List[uuid.UUID]:
        """
        Index chunks to Qdrant using batch upsert.

        Args:
            chunks: List of text chunks
            file_id: File identifier
            file_name: Original filename
            user_id: User who uploaded
            file_type: File extension
            file_size: File size in bytes

        Returns:
            List of Qdrant point IDs
        """
        if not chunks:
            logger.warning("No chunks to index")
            return []

        try:
            # Prepare batch data
            metadatas = []
            for idx in range(len(chunks)):
                metadatas.append({
                    "file_id": file_id,
                    "file_name": file_name,
                    "chunk_index": idx,
                    "uploaded_by": user_id,
                    "uploaded_at": datetime.utcnow().isoformat(),
                    "file_type": file_type,
                    "file_size": file_size
                })

            # Batch upsert to Qdrant
            point_ids = await self.qdrant_service.upsert_batch(chunks, metadatas)
            
            logger.info(f"Batch indexed {len(point_ids)} chunks")
            return point_ids
            
        except Exception as e:
            logger.error(f"Failed to batch index: {e}")
            raise
    
    def get_ingestion_logs(
        self,
        user_id: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[IngestionLog]:
        """
        Get ingestion logs with filtering.
        
        Args:
            user_id: Filter by user
            status: Filter by status
            limit: Maximum results
            offset: Result offset
            
        Returns:
            List of IngestionLog
        """
        query = self.db.query(IngestionLog)
        
        if user_id:
            query = query.filter(IngestionLog.user_id == user_id)
        
        if status:
            query = query.filter(IngestionLog.status == status)
        
        query = query.order_by(IngestionLog.created_at.desc())
        query = query.offset(offset).limit(limit)
        
        return query.all()
    
    def get_ingestion_log(self, log_id: uuid.UUID) -> Optional[IngestionLog]:
        """
        Get single ingestion log by ID.
        
        Args:
            log_id: Log ID
            
        Returns:
            IngestionLog or None
        """
        return self.db.query(IngestionLog).filter(IngestionLog.id == log_id).first()
    
    def delete_ingestion_log(self, log_id: uuid.UUID) -> bool:
        """
        Delete ingestion log and associated Qdrant points.
        
        Args:
            log_id: Log ID
            
        Returns:
            True if deleted
        """
        log = self.get_ingestion_log(log_id)
        if not log:
            return False
        
        # Delete from Qdrant
        if log.qdrant_point_ids:
            try:
                point_ids = json.loads(log.qdrant_point_ids)
                for point_id in point_ids:
                    self.qdrant_service.delete(uuid.UUID(point_id))
            except Exception as e:
                logger.error(f"Failed to delete Qdrant points: {e}")
        
        # Delete log
        self.db.delete(log)
        self.db.commit()
        
        logger.info(f"Deleted ingestion log {log_id}")
        return True
