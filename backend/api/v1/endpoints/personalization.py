"""
Personalization API endpoints for Phase 7 - Final Intelligence.

Provides REST API for hardware-aware content personalization.
"""

import logging
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from db.session import get_db
from auth.middleware import require_auth, UserContext
from models.user import User
from schemas.personalization import ChapterSummaryResponse, PersonalizationRegenerateRequest
from services.personalization_service import PersonalizationService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1", tags=["Personalization"])


@router.get("/chapters/{chapter_id}/summary", response_model=ChapterSummaryResponse)
async def get_chapter_summary(
    chapter_id: UUID,
    hardware_profile: Optional[str] = None,
    skill_level: Optional[str] = None,
    current_user: UserContext = Depends(require_auth),
    db: Session = Depends(get_db),
):
    """
    Get personalized chapter summary based on user's hardware and skill level.

    If hardware_profile or skill_level not provided as query params,
    uses current user's profile from authentication context.
    """
    logger.info(f"Getting summary for chapter {chapter_id}")

    # Get user's profile if not provided in query params
    if not hardware_profile or not skill_level:
        # Query user's student profile
        from models.student_profile import StudentProfile
        from sqlalchemy import select

        stmt = select(StudentProfile).where(StudentProfile.user_id == current_user.user_id)
        student_profile = db.execute(stmt).scalars().first()

        if student_profile:
            if not hardware_profile:
                # Get from hardware config
                if student_profile.hardware_config:
                    hardware_profile = student_profile.hardware_config.hardware_type
                else:
                    hardware_profile = "sim_rig"  # Default

            if not skill_level:
                skill_level = student_profile.skill_level
        else:
            # Defaults for unauthenticated or no profile
            hardware_profile = hardware_profile or "sim_rig"
            skill_level = skill_level or "beginner"

    logger.info(f"Using hardware_profile={hardware_profile}, skill_level={skill_level}")

    service = PersonalizationService(db)
    result = await service.get_or_generate_summary(chapter_id, hardware_profile, skill_level)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Chapter {chapter_id} not found"
        )

    return ChapterSummaryResponse(
        chapter_id=str(chapter_id),
        summary_content=result["summary_content"],
        hardware_profile_type=result["hardware_profile_type"],
        skill_level=result["skill_level"],
        generated_at=result["generated_at"],
    )


@router.post("/personalization/regenerate")
async def regenerate_summaries(
    request: PersonalizationRegenerateRequest,
    current_user: UserContext = Depends(require_auth),
    db: Session = Depends(get_db),
):
    """
    Regenerate all personalized summaries (admin only).

    Can filter by specific hardware profile or skill level.
    """
    # Admin-only check
    db_user = db.query(User).filter(User.id == current_user.user_id).first()
    if not db_user or not db_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required for bulk regeneration"
        )

    logger.info("Regenerating summaries (admin operation)")

    service = PersonalizationService(db)

    try:
        count = await service.regenerate_all_summaries(
            hardware_profile_type=request.hardware_profile,
            skill_level=request.skill_level,
        )

        return {
            "status": "success",
            "message": f"Regenerated {count} summaries",
            "count": count,
        }

    except Exception as e:
        logger.error(f"Failed to regenerate summaries: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to regenerate summaries: {str(e)}"
        )
