"""
Curriculum service for Phase 7 - Final Intelligence.

Manages 13-week curriculum content ingestion and retrieval.
"""

import logging
import re
from pathlib import Path
from typing import List, Optional, Dict, Any
from uuid import UUID

from sqlalchemy.orm import Session
from sqlalchemy import and_

from models.curriculum import CurriculumWeek, Chapter
from models.ingestion_log import IngestionLog

logger = logging.getLogger(__name__)


class CurriculumService:
    """
    Service for managing curriculum content.

    Provides:
    - Batch ingestion of 13-week curriculum
    - Week and chapter retrieval
    - Integration with personalization service
    """

    def __init__(self, db: Session):
        """
        Initialize curriculum service.

        Args:
            db: Database session
        """
        self.db = db

    def parse_markdown_frontmatter(self, content: str) -> Dict[str, Any]:
        """
        Parse YAML frontmatter from markdown content.

        Args:
            content: Markdown content with frontmatter

        Returns:
            Dictionary with frontmatter metadata
        """
        frontmatter = {}

        # Extract frontmatter between --- markers
        match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        if match:
            frontmatter_text = match.group(1)
            # Simple YAML parsing for key-value pairs
            for line in frontmatter_text.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    key = key.strip()
                    value = value.strip().strip('"\'')
                    # Handle arrays
                    if value.startswith('[') and value.endswith(']'):
                        value = [v.strip() for v in value[1:-1].split(',')]
                    frontmatter[key] = value

        return frontmatter

    def extract_metadata(self, file_path: Path, content: str) -> Dict[str, Any]:
        """
        Extract metadata from markdown file.

        Args:
            file_path: Path to markdown file
            content: File content

        Returns:
            Dictionary with chapter metadata
        """
        frontmatter = self.parse_markdown_frontmatter(content)

        # Extract title from frontmatter or first H1
        title = frontmatter.get('title', '')
        if not title:
            h1_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
            if h1_match:
                title = h1_match.group(1)

        # Extract chapter_id from frontmatter or filename
        chapter_id = frontmatter.get('id', file_path.stem)

        # Extract tags
        tags = frontmatter.get('tags', [])
        if isinstance(tags, str):
            tags = [tags]

        # Extract week number
        week_number = frontmatter.get('week_number')
        if not week_number:
            # Try to extract from filename (week-1, week-2, etc.)
            week_match = re.search(r'week-(\d+)', file_path.stem)
            if week_match:
                week_number = int(week_match.group(1))

        return {
            'chapter_id': chapter_id,
            'title': title,
            'content': content,
            'week_number': week_number,
            'tags': tags,
            'estimated_time': frontmatter.get('estimated_time'),
            'hardware_relevant': frontmatter.get('hardware_relevant', ['sim_rig', 'edge_kit']),
        }

    def ingest_chapter(self, file_path: Path, content: str) -> Optional[UUID]:
        """
        Ingest a single chapter from markdown file.

        Args:
            file_path: Path to markdown file
            content: File content

        Returns:
            Chapter UUID if successful, None otherwise
        """
        logger.info(f"Ingesting chapter from {file_path}")

        try:
            # Extract metadata
            metadata = self.extract_metadata(file_path, content)

            # Get or create CurriculumWeek
            week = None
            if metadata['week_number']:
                week = self.db.query(CurriculumWeek).filter(
                    CurriculumWeek.week_number == metadata['week_number']
                ).first()

                if not week:
                    week = CurriculumWeek(
                        week_number=metadata['week_number'],
                        title=f"Week {metadata['week_number']}",
                        description="",
                        sort_order=metadata['week_number'],
                    )
                    self.db.add(week)
                    self.db.flush()
                    logger.info(f"Created CurriculumWeek {metadata['week_number']}")

            # Create or update Chapter
            chapter = self.db.query(Chapter).filter(
                Chapter.title == metadata['title']
            ).first()

            if chapter:
                # Update existing
                chapter.content = metadata['content']
                chapter.tags = metadata['tags']
                chapter.hardware_relevant = metadata['hardware_relevant']
            else:
                # Create new
                chapter = Chapter(
                    curriculum_week_id=week.id if week else None,
                    title=metadata['title'],
                    content=metadata['content'],
                    sort_order=1,  # Use sort_order not 'order'
                    tags=metadata['tags'],
                    hardware_relevant=metadata['hardware_relevant'],
                )
                self.db.add(chapter)

            self.db.commit()
            self.db.refresh(chapter)

            logger.info(f"Ingested chapter {chapter.id} - {chapter.title}")

            # Log ingestion
            self._log_ingestion(chapter.id, 'success', 1, 0)

            return chapter.id

        except Exception as e:
            logger.error(f"Failed to ingest chapter: {e}")
            self.db.rollback()
            self._log_ingestion(None, 'failed', 0, 0, str(e))
            return None

    def _log_ingestion(
        self,
        chapter_id: Optional[UUID],
        status: str,
        chunks: int,
        vectors: int,
        error_message: Optional[str] = None,
    ):
        """
        Log ingestion attempt to IngestionLog table.

        Args:
            chapter_id: Chapter UUID or None
            status: 'success' or 'failed'
            chunks: Number of chunks processed
            vectors: Number of vectors upserted
            error_message: Error message if failed
        """
        try:
            log = IngestionLog(
                chapter_id=chapter_id,
                status=status,
                chunks_processed=chunks,
                vectors_upserted=vectors,
                error_message=error_message,
            )
            self.db.add(log)
            self.db.commit()
        except Exception as e:
            logger.error(f"Failed to log ingestion: {e}")
            self.db.rollback()

    async def ingest_week(self, week_data: dict) -> dict:
        """
        Ingest a single week of curriculum content.

        Args:
            week_data: Dictionary with week_number, title, description, chapters

        Returns:
            Dictionary with ingested week details
        """
        logger.info(f"Ingesting week {week_data.get('week_number')}")

        # Get or create CurriculumWeek
        week = self.db.query(CurriculumWeek).filter(
            CurriculumWeek.week_number == week_data['week_number']
        ).first()

        if not week:
            week = CurriculumWeek(
                week_number=week_data['week_number'],
                title=week_data['title'],
                description=week_data.get('description', ''),
                sort_order=week_data['week_number'],
            )
            self.db.add(week)
            self.db.commit()
            self.db.refresh(week)

        # Process chapters
        chapters_ingested = []
        for chapter_data in week_data.get('chapters', []):
            chapter = Chapter(
                curriculum_week_id=week.id,
                title=chapter_data['title'],
                content=chapter_data['content'],
                sort_order=chapter_data.get('order', 1),
            )
            self.db.add(chapter)
            chapters_ingested.append(chapter.id)

        self.db.commit()

        return {
            'week_id': str(week.id),
            'week_number': week.week_number,
            'chapters_ingested': len(chapters_ingested),
        }

    def get_all_weeks(self, include_chapters: bool = False) -> List[dict]:
        """
        Get all curriculum weeks.

        Args:
            include_chapters: Whether to include chapter list

        Returns:
            List of week dictionaries
        """
        logger.info("Getting all weeks")

        weeks = self.db.query(CurriculumWeek).order_by(CurriculumWeek.week_number).all()

        result = []
        for week in weeks:
            week_dict = {
                'id': str(week.id),
                'week_number': week.week_number,
                'title': week.title,
                'description': week.description,
            }

            if include_chapters:
                week_dict['chapters'] = [
                    {
                        'id': str(chapter.id),
                        'title': chapter.title,
                        'order': chapter.sort_order,
                    }
                    for chapter in week.chapters
                ]

            result.append(week_dict)

        return result

    def get_week_by_number(self, week_number: int) -> Optional[dict]:
        """
        Get specific week by week number.

        Args:
            week_number: Week number (1-13)

        Returns:
            Week dictionary with chapters, or None if not found
        """
        logger.info(f"Getting week {week_number}")

        week = self.db.query(CurriculumWeek).filter(
            CurriculumWeek.week_number == week_number
        ).first()

        if not week:
            return None

        return {
            'id': str(week.id),
            'week_number': week.week_number,
            'title': week.title,
            'description': week.description,
            'chapters': [
                {
                    'id': str(chapter.id),
                    'title': chapter.title,
                    'content': chapter.content,
                    'order': chapter.sort_order,
                }
                for chapter in week.chapters
            ],
        }

    def get_chapter_by_id(self, chapter_id: UUID) -> Optional[dict]:
        """
        Get chapter by ID.

        Args:
            chapter_id: Chapter identifier

        Returns:
            Chapter dictionary with content, or None if not found
        """
        logger.info(f"Getting chapter {chapter_id}")

        chapter = self.db.query(Chapter).filter(Chapter.id == chapter_id).first()

        if not chapter:
            return None

        return {
            'id': str(chapter.id),
            'title': chapter.title,
            'content': chapter.content,
            'tags': chapter.tags,
            'hardware_relevant': chapter.hardware_relevant,
        }

    async def regenerate_all_summaries(self) -> int:
        """
        Regenerate all personalized summaries for all chapters.

        Returns:
            Number of summaries generated
        """
        logger.info("Regenerating all summaries")

        # TODO: Implement using PersonalizationService

        return 0
