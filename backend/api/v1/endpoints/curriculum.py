"""
Curriculum API endpoints for Phase 7 - Final Intelligence.

Provides REST API for curriculum content access.
"""

import logging
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from db.session import get_db
from auth.middleware import require_auth, UserContext
from models.user import User
from services.curriculum_service import CurriculumService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/curriculum", tags=["Curriculum"])


class ChapterIngestRequest(BaseModel):
    title: str
    content: str
    order: int = 1
    estimated_time: Optional[str] = None
    tags: List[str] = []
    hardware_relevant: List[str] = ["sim_rig", "edge_kit"]


class WeekIngestRequest(BaseModel):
    week_number: int
    title: str
    description: str = ""
    chapters: List[ChapterIngestRequest] = []


@router.post("/ingest", response_model=dict)
async def ingest_curriculum(
    weeks: List[WeekIngestRequest],
    current_user: UserContext = Depends(require_auth),
    db: Session = Depends(get_db),
):
    """
    Batch ingest curriculum weeks (admin only).

    Accepts list of weeks with chapters and stores in database.
    """
    db_user = db.query(User).filter(User.id == current_user.user_id).first()
    if not db_user or not db_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required for curriculum ingestion"
        )

    logger.info(f"Starting batch curriculum ingestion: {len(weeks)} weeks")

    service = CurriculumService(db)
    results = []

    for week_data in weeks:
        try:
            result = await service.ingest_week(week_data.model_dump())
            results.append(result)
            logger.info(f"Ingested week {week_data.week_number}: {week_data.title}")
        except Exception as e:
            logger.error(f"Failed to ingest week {week_data.week_number}: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to ingest week {week_data.week_number}: {str(e)}"
            )

    return {
        "status": "success",
        "weeks_ingested": len(results),
        "results": results,
    }


@router.get("/weeks", response_model=List[dict])
async def get_all_weeks(
    include_chapters: bool = Query(False, description="Include chapter list"),
    db: Session = Depends(get_db),
):
    """
    Get all curriculum weeks.

    Returns list of all 13 weeks with optional chapter details.
    """
    logger.info("Getting all curriculum weeks")

    service = CurriculumService(db)
    weeks = service.get_all_weeks(include_chapters=include_chapters)

    return weeks


@router.get("/weeks/{week_number}", response_model=dict)
async def get_week(
    week_number: int,
    db: Session = Depends(get_db),
):
    """
    Get specific week by week number.

    Returns week details with all chapters and their content.
    """
    logger.info(f"Getting week {week_number}")

    service = CurriculumService(db)
    week = service.get_week_by_number(week_number)

    if not week:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Week {week_number} not found"
        )

    return week


@router.get("/chapters/{chapter_id}", response_model=dict)
async def get_chapter(
    chapter_id: UUID,
    db: Session = Depends(get_db),
):
    """
    Get chapter by ID.

    Returns chapter content with metadata.
    """
    logger.info(f"Getting chapter {chapter_id}")

    service = CurriculumService(db)
    chapter = service.get_chapter_by_id(chapter_id)

    if not chapter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chapter not found"
        )

    return chapter
