"""
Personalization service for Phase 7 - Final Intelligence.

Generates hardware-aware and skill-level-aware chapter summaries using Grok API.
"""

import logging
from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session
from sqlalchemy import and_

from models.curriculum import Chapter, ChapterSummary
from llm.grok_client import GrokClient, GrokAPIError
from llm.prompts.personalization import PERSONALIZATION_PROMPT_TEMPLATE

logger = logging.getLogger(__name__)


class PersonalizationService:
    """
    Service for generating personalized chapter summaries.
    
    Uses Grok API to rewrite chapter summaries based on:
    - User's hardware profile (sim_rig, edge_kit, unitree)
    - User's skill level (beginner, intermediate, advanced)
    
    Summaries are cached in the database to avoid redundant API calls.
    """
    
    def __init__(self, db: Session):
        """
        Initialize personalization service.
        
        Args:
            db: Database session
        """
        self.db = db
        self.grok_client = GrokClient()
    
    async def get_or_generate_summary(
        self,
        chapter_id: UUID,
        hardware_profile_type: str,
        skill_level: str,
    ) -> Optional[dict]:
        """
        Get cached summary or generate new one using Grok API.
        
        Args:
            chapter_id: Chapter identifier
            hardware_profile_type: Hardware profile (sim_rig, edge_kit, unitree)
            skill_level: Skill level (beginner, intermediate, advanced)
            
        Returns:
            Dictionary with summary_content, generated_at, or None if chapter not found
        """
        logger.info(
            f"Getting summary for chapter={chapter_id}, "
            f"hardware={hardware_profile_type}, skill={skill_level}"
        )
        
        # Step 1: Check database cache
        cached_summary = self._get_cached_summary(
            chapter_id, hardware_profile_type, skill_level
        )
        
        if cached_summary:
            logger.info(f"Found cached summary for chapter {chapter_id}")
            return {
                "summary_content": cached_summary.summary_content,
                "generated_at": cached_summary.generated_at.isoformat(),
                "hardware_profile_type": cached_summary.hardware_profile_type,
                "skill_level": cached_summary.skill_level,
            }
        
        # Step 2: Get chapter content
        chapter = self.db.query(Chapter).filter(Chapter.id == chapter_id).first()
        if not chapter:
            logger.error(f"Chapter {chapter_id} not found")
            return None
        
        # Step 3: Generate summary using Grok API
        try:
            logger.info(f"Generating new summary for chapter {chapter_id}")
            
            # Build hardware details
            hardware_details = {}
            if hardware_profile_type == 'sim_rig':
                hardware_details = {
                    'gpu_model': 'RTX 4070 Ti or better',
                    'gpu_vram_gb': '16+',
                    'ubuntu_version': '22.04+',
                }
            elif hardware_profile_type == 'edge_kit':
                hardware_details = {
                    'edge_kit_type': 'Jetson Orin Nano/NX',
                    'jetpack_version': '5.1+',
                    'ubuntu_version': '22.04',
                }
            elif hardware_profile_type == 'unitree':
                hardware_details = {
                    'robot_model': 'Unitree Go2/G1',
                }
            
            # Call Grok API
            result = await self.grok_client.generate_personalized_summary(
                system_prompt=PERSONALIZATION_PROMPT_TEMPLATE,
                chapter_content=chapter.content[:8000],  # Limit content length
                hardware_type=hardware_profile_type,
                skill_level=skill_level,
                hardware_details=hardware_details,
            )
            
            # Step 4: Save to database
            summary = self._save_summary(
                chapter_id=chapter_id,
                hardware_profile_type=hardware_profile_type,
                skill_level=skill_level,
                summary_content=result["summary_content"],
                generated_by="grok-2",
                token_count=result["tokens_used"],
            )
            
            logger.info(
                f"Generated and saved summary for chapter {chapter_id} "
                f"(tokens: {result['tokens_used']}, time: {result['generation_time_ms']:.0f}ms)"
            )
            
            return {
                "summary_content": summary.summary_content,
                "generated_at": summary.generated_at.isoformat(),
                "hardware_profile_type": summary.hardware_profile_type,
                "skill_level": summary.skill_level,
            }
            
        except GrokAPIError as e:
            logger.error(f"Grok API error for chapter {chapter_id}: {e}")
            # Return cached summary if available, even if old
            if cached_summary:
                logger.warning("Returning stale cached summary due to API error")
                return {
                    "summary_content": cached_summary.summary_content,
                    "generated_at": cached_summary.generated_at.isoformat(),
                    "hardware_profile_type": cached_summary.hardware_profile_type,
                    "skill_level": cached_summary.skill_level,
                }
            raise
    
    def _get_cached_summary(
        self,
        chapter_id: UUID,
        hardware_profile_type: str,
        skill_level: str,
    ) -> Optional[ChapterSummary]:
        """
        Get cached summary from database.
        
        Args:
            chapter_id: Chapter identifier
            hardware_profile_type: Hardware profile
            skill_level: Skill level
            
        Returns:
            ChapterSummary if found, None otherwise
        """
        return self.db.query(ChapterSummary).filter(
            and_(
                ChapterSummary.chapter_id == chapter_id,
                ChapterSummary.hardware_profile_type == hardware_profile_type,
                ChapterSummary.skill_level == skill_level,
            )
        ).first()
    
    def _save_summary(
        self,
        chapter_id: UUID,
        hardware_profile_type: str,
        skill_level: str,
        summary_content: str,
        generated_by: str,
        token_count: int,
    ) -> ChapterSummary:
        """
        Save generated summary to database.
        
        Args:
            chapter_id: Chapter identifier
            hardware_profile_type: Hardware profile
            skill_level: Skill level
            summary_content: Generated summary content
            generated_by: LLM model identifier
            token_count: Tokens used
            
        Returns:
            Saved ChapterSummary instance
        """
        summary = ChapterSummary(
            chapter_id=chapter_id,
            hardware_profile_type=hardware_profile_type,
            skill_level=skill_level,
            summary_content=summary_content,
            generated_by=generated_by,
            token_count=token_count,
        )
        
        self.db.add(summary)
        self.db.commit()
        self.db.refresh(summary)
        
        return summary
    
    async def regenerate_all_summaries(
        self,
        hardware_profile_type: Optional[str] = None,
        skill_level: Optional[str] = None,
    ) -> int:
        """
        Regenerate all chapter summaries (admin operation).
        
        Args:
            hardware_profile_type: Filter by hardware type (optional)
            skill_level: Filter by skill level (optional)
            
        Returns:
            Number of summaries regenerated
        """
        logger.info("Regenerating all summaries (admin operation)")
        
        # Get all chapters
        query = self.db.query(Chapter)
        chapters = query.all()
        
        # Hardware profiles and skill levels to generate
        hardware_profiles = ['sim_rig', 'edge_kit', 'unitree']
        skill_levels = ['beginner', 'intermediate', 'advanced']
        
        # Filter if specified
        if hardware_profile_type:
            hardware_profiles = [hardware_profile_type]
        if skill_level:
            skill_levels = [skill_level]
        
        regenerated_count = 0
        
        for chapter in chapters:
            for hw_profile in hardware_profiles:
                for skill in skill_levels:
                    try:
                        await self.get_or_generate_summary(
                            chapter_id=chapter.id,
                            hardware_profile_type=hw_profile,
                            skill_level=skill,
                        )
                        regenerated_count += 1
                    except Exception as e:
                        logger.error(
                            f"Failed to regenerate summary for chapter {chapter.id}, "
                            f"hw={hw_profile}, skill={skill}: {e}"
                        )
        
        logger.info(f"Regenerated {regenerated_count} summaries")
        return regenerated_count
