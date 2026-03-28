"""
Translation service for Phase 7 - Final Intelligence.

Provides Roman Urdu translation of chapter content using Grok API.
"""

import logging
from datetime import datetime, timedelta
from typing import Optional, List
from uuid import UUID

from sqlalchemy.orm import Session
from sqlalchemy import and_, func

from models.curriculum import Chapter, Translation
from llm.grok_client import GrokClient, GrokAPIError
from llm.prompts.translation import (
    TRANSLATION_PROMPT_TEMPLATE,
    TECHNICAL_TERMS_PRESERVATION,
    validate_translation_preservation,
)

logger = logging.getLogger(__name__)


class TranslationService:
    """
    Service for translating chapter content to Roman Urdu.

    Uses Grok API with preservation rules to:
    - Translate explanatory prose to Roman Urdu
    - Preserve code blocks, technical terms, and API names
    - Maintain markdown formatting

    Translations are stored with status tracking (draft/in_review/published).
    """

    def __init__(self, db: Session):
        """
        Initialize translation service.

        Args:
            db: Database session
        """
        self.db = db
        self.grok_client = GrokClient()

    async def get_translation(
        self,
        chapter_id: UUID,
        language_code: str = "ur-Latn",
    ) -> Optional[dict]:
        """
        Get translation for a chapter.

        Args:
            chapter_id: Chapter identifier
            language_code: Language code (default: ur-Latn for Roman Urdu)

        Returns:
            Dictionary with translated_content, status, updated_at, or None if not found
        """
        logger.info(f"Getting translation for chapter={chapter_id}, lang={language_code}")

        # Step 1: Check database cache
        cached_translation = self._get_cached_translation(chapter_id, language_code)

        if cached_translation:
            # Check if draft is too old (regenerate if older than 7 days)
            if cached_translation.status == 'draft':
                age = datetime.utcnow() - cached_translation.updated_at
                if age > timedelta(days=7):
                    logger.info(f"Draft translation too old ({age}), regenerating")
                    return await self._generate_and_save_translation(chapter_id, language_code)

            logger.info(f"Found cached translation for chapter {chapter_id} (status: {cached_translation.status})")
            return {
                "translated_content": cached_translation.translated_content,
                "status": cached_translation.status,
                "updated_at": cached_translation.updated_at.isoformat(),
                "language_code": cached_translation.language_code,
            }

        # Step 2: Generate new translation
        logger.info(f"No cached translation found, generating for chapter {chapter_id}")
        return await self._generate_and_save_translation(chapter_id, language_code)

    async def _generate_and_save_translation(
        self,
        chapter_id: UUID,
        language_code: str,
    ) -> Optional[dict]:
        """
        Generate translation using Grok API and save to database.

        Args:
            chapter_id: Chapter identifier
            language_code: Language code

        Returns:
            Dictionary with translation details or None if chapter not found
        """
        # Get chapter content
        chapter = self.db.query(Chapter).filter(Chapter.id == chapter_id).first()
        if not chapter:
            logger.error(f"Chapter {chapter_id} not found")
            return None

        try:
            # Call Grok API
            result = await self.grok_client.generate_translation(
                system_prompt=TRANSLATION_PROMPT_TEMPLATE,
                content=chapter.content[:12000],  # Limit content length
                language_code=language_code,
            )

            # Validate technical term preservation
            validation_issues = validate_translation_preservation(
                result["translated_content"],
                chapter.content
            )

            if validation_issues:
                logger.warning(f"Translation validation issues: {validation_issues[:5]}")

            # Save to database
            translation = self._save_translation(
                chapter_id=chapter_id,
                language_code=language_code,
                translated_content=result["translated_content"],
                status="draft",  # AI-generated translations start as draft
                translated_by="grok-2-ai",
            )

            logger.info(
                f"Generated and saved translation for chapter {chapter_id} "
                f"(tokens: {result['tokens_used']}, time: {result['generation_time_ms']:.0f}ms)"
            )

            return {
                "translated_content": translation.translated_content,
                "status": translation.status,
                "updated_at": translation.updated_at.isoformat(),
                "language_code": translation.language_code,
            }

        except GrokAPIError as e:
            logger.error(f"Grok API error for chapter {chapter_id}: {e}")
            # Return None to trigger "AI Translation in progress" indicator
            return None

    def _get_cached_translation(
        self,
        chapter_id: UUID,
        language_code: str,
    ) -> Optional[Translation]:
        """
        Get cached translation from database.

        Args:
            chapter_id: Chapter identifier
            language_code: Language code

        Returns:
            Translation if found, None otherwise
        """
        return self.db.query(Translation).filter(
            and_(
                Translation.chapter_id == chapter_id,
                Translation.language_code == language_code,
            )
        ).first()

    def _save_translation(
        self,
        chapter_id: UUID,
        language_code: str,
        translated_content: str,
        status: str,
        translated_by: str,
        review_notes: Optional[str] = None,
    ) -> Translation:
        """
        Save translation to database.

        Args:
            chapter_id: Chapter identifier
            language_code: Language code
            translated_content: Translated content
            status: Translation status
            translated_by: Source identifier
            review_notes: Admin review notes

        Returns:
            Saved Translation instance
        """
        # Check if translation exists
        existing = self._get_cached_translation(chapter_id, language_code)

        if existing:
            # Update existing
            existing.translated_content = translated_content
            existing.status = status
            existing.translated_by = translated_by
            existing.review_notes = review_notes
            translation = existing
        else:
            # Create new
            translation = Translation(
                chapter_id=chapter_id,
                language_code=language_code,
                translated_content=translated_content,
                status=status,
                translated_by=translated_by,
                review_notes=review_notes,
            )
            self.db.add(translation)

        self.db.commit()
        self.db.refresh(translation)

        return translation

    async def create_or_update_translation(
        self,
        chapter_id: UUID,
        language_code: str,
        translated_content: Optional[str] = None,
        status: str = "draft",
        translated_by: Optional[str] = None,
        review_notes: Optional[str] = None,
    ) -> dict:
        """
        Create or update translation (admin operation).

        Args:
            chapter_id: Chapter identifier
            language_code: Language code
            translated_content: Translated markdown content (if None, generate via API)
            status: Translation status (draft/in_review/published)
            translated_by: Source identifier (e.g., "grok-2-ai", user ID)
            review_notes: Admin review notes

        Returns:
            Dictionary with translation details
        """
        logger.info(f"Creating/updating translation for chapter={chapter_id}")

        # Generate via API if content not provided
        if not translated_content:
            result = await self.get_translation(chapter_id, language_code)
            if not result:
                raise ValueError("Failed to generate translation")
            translated_content = result["translated_content"]
            translated_by = translated_by or "grok-2-ai"
            status = status or "draft"

        # Save translation
        translation = self._save_translation(
            chapter_id=chapter_id,
            language_code=language_code,
            translated_content=translated_content,
            status=status,
            translated_by=translated_by or "admin",
            review_notes=review_notes,
        )

        logger.info(f"Translation saved for chapter {chapter_id} with status {status}")

        return {
            "translated_content": translation.translated_content,
            "status": translation.status,
            "updated_at": translation.updated_at.isoformat(),
            "language_code": translation.language_code,
        }

    async def get_translation_stats(self) -> dict:
        """
        Get translation coverage statistics.

        Returns:
            Dictionary with total_chapters, translated_chapters, coverage_percentage, by_language
        """
        logger.info("Getting translation statistics")

        # Get total chapters
        total_chapters = self.db.query(Chapter).count()

        # Get translation counts by status
        stats_query = self.db.query(
            Translation.language_code,
            Translation.status,
            func.count(Translation.id).label('count'),
        ).group_by(Translation.language_code, Translation.status).all()

        # Aggregate statistics
        by_language = {}
        total_translated = 0
        total_published = 0
        total_draft = 0

        for row in stats_query:
            lang = row.language_code
            status = row.status
            count = row.count

            if lang not in by_language:
                by_language[lang] = {
                    "published": 0,
                    "draft": 0,
                    "in_review": 0,
                }

            by_language[lang][status] = count

            if status == 'published':
                total_published += count
            elif status == 'draft':
                total_draft += count

            total_translated += count

        coverage_percentage = (total_published / total_chapters * 100) if total_chapters > 0 else 0.0

        return {
            "total_chapters": total_chapters,
            "translated_chapters": total_translated,
            "published_chapters": total_published,
            "draft_chapters": total_draft,
            "coverage_percentage": round(coverage_percentage, 2),
            "by_language": by_language,
        }
