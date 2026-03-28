"""
Translation API endpoints for Phase 7 - Final Intelligence.

Provides REST API for Roman Urdu translation management.
"""

import logging
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from db.session import get_db
from auth.middleware import require_auth, UserContext
from models.user import User
from schemas.translation import TranslationResponse, TranslationUpdate, TranslationStatsResponse
from services.translation_service import TranslationService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1", tags=["Translations"])


@router.get("/chapters/{chapter_id}/translation", response_model=TranslationResponse)
async def get_chapter_translation(
    chapter_id: UUID,
    lang: str = "ur-Latn",
    current_user: UserContext = Depends(require_auth),
    db: Session = Depends(get_db),
):
    """
    Get Roman Urdu translation for a chapter.

    Returns 404 if translation not found (triggers "AI Translation in progress" indicator).
    """
    logger.info(f"Getting translation for chapter {chapter_id}, lang={lang}")

    service = TranslationService(db)
    result = await service.get_translation(chapter_id, lang)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": "translation_not_found",
                "message": "Translation not available yet. AI translation in progress.",
                "language_code": lang,
            }
        )

    return TranslationResponse(
        chapter_id=str(chapter_id),
        translated_content=result["translated_content"],
        language_code=result["language_code"],
        status=result["status"],
        updated_at=result["updated_at"],
    )


@router.put("/chapters/{chapter_id}/translation", response_model=TranslationResponse)
async def update_chapter_translation(
    chapter_id: UUID,
    translation_data: TranslationUpdate,
    current_user: UserContext = Depends(require_auth),
    db: Session = Depends(get_db),
):
    """
    Update or create translation (admin only).

    Supports manual translation updates by admins or AI-generated translations.
    """
    # Admin-only check
    db_user = db.query(User).filter(User.id == current_user.user_id).first()
    if not db_user or not db_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required for translation updates"
        )

    logger.info(f"Updating translation for chapter {chapter_id} by admin {current_user.user_id}")

    service = TranslationService(db)

    try:
        result = await service.create_or_update_translation(
            chapter_id=chapter_id,
            language_code=translation_data.language_code,
            translated_content=translation_data.translated_content,
            status=translation_data.status.value if translation_data.status else "draft",
            translated_by=str(current_user.user_id),
            review_notes=translation_data.review_notes,
        )

        return TranslationResponse(
            chapter_id=str(chapter_id),
            translated_content=result["translated_content"],
            language_code=result["language_code"],
            status=result["status"],
            updated_at=result["updated_at"],
        )

    except ValueError as e:
        logger.error(f"Failed to update translation: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update translation: {str(e)}"
        )


@router.get("/translations/status", response_model=TranslationStatsResponse)
async def get_translation_status(
    current_user: UserContext = Depends(require_auth),
    db: Session = Depends(get_db),
):
    """
    Get translation coverage statistics.

    Shows how many chapters have been translated and their status.
    """
    logger.info("Getting translation statistics")

    service = TranslationService(db)
    stats = await service.get_translation_stats()

    return TranslationStatsResponse(
        total_chapters=stats["total_chapters"],
        translated_chapters=stats["translated_chapters"],
        published_chapters=stats["published_chapters"],
        draft_chapters=stats["draft_chapters"],
        coverage_percentage=stats["coverage_percentage"],
        by_language=stats["by_language"],
    )
