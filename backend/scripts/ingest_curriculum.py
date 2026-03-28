#!/usr/bin/env python3
"""
Curriculum ingestion script for Phase 7 - Final Intelligence.

Ingests all markdown files from docs/ directory into PostgreSQL and Qdrant.

Usage:
    python -m scripts.ingest_curriculum --docs-path ../docusaurus-textbook/docs
"""

import argparse
import logging
from pathlib import Path
from datetime import datetime

from sqlalchemy.orm import Session
from db.session import get_db
from services.curriculum_service import CurriculumService

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def ingest_all_docs(docs_path: Path, db: Session):
    """
    Ingest all markdown files from docs directory.

    Args:
        docs_path: Path to docs directory
        db: Database session
    """
    logger.info(f"Starting curriculum ingestion from {docs_path}")

    service = CurriculumService(db)

    # Find all markdown files
    markdown_files = list(docs_path.glob('**/*.md'))
    logger.info(f"Found {len(markdown_files)} markdown files")

    # Ingest each file
    ingested_count = 0
    failed_count = 0

    for md_file in sorted(markdown_files):
        logger.info(f"Processing {md_file.name}...")

        try:
            # Read content
            content = md_file.read_text(encoding='utf-8')

            # Ingest chapter
            chapter_id = service.ingest_chapter(md_file, content)

            if chapter_id:
                ingested_count += 1
                logger.info(f"✓ Successfully ingested {md_file.name}")
            else:
                failed_count += 1
                logger.error(f"✗ Failed to ingest {md_file.name}")

        except Exception as e:
            failed_count += 1
            logger.error(f"✗ Error processing {md_file.name}: {e}")

    # Summary
    logger.info("=" * 60)
    logger.info(f"Ingestion Summary:")
    logger.info(f"  Total files processed: {len(markdown_files)}")
    logger.info(f"  Successfully ingested: {ingested_count}")
    logger.info(f"  Failed: {failed_count}")
    logger.info(f"  Success rate: {ingested_count / len(markdown_files) * 100:.1f}%")
    logger.info("=" * 60)

    # Verify ingestion
    logger.info("Verifying ingestion...")
    weeks = service.get_all_weeks(include_chapters=True)
    logger.info(f"  Curriculum weeks in database: {len(weeks)}")

    for week in weeks:
        logger.info(f"  - Week {week['week_number']}: {week['title']} ({len(week.get('chapters', []))} chapters)")

    return ingested_count, failed_count


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='Ingest curriculum content')
    parser.add_argument(
        '--docs-path',
        type=str,
        default='../docusaurus-textbook/docs',
        help='Path to docs directory containing markdown files'
    )
    parser.add_argument(
        '--db-url',
        type=str,
        default=None,
        help='Database URL (optional, uses config if not provided)'
    )

    args = parser.parse_args()

    # Resolve docs path
    docs_path = Path(args.docs_path).resolve()
    if not docs_path.exists():
        logger.error(f"Docs path does not exist: {docs_path}")
        return 1

    logger.info(f"Using docs path: {docs_path}")

    # Get database session
    db = next(get_db())

    try:
        # Run ingestion
        start_time = datetime.utcnow()
        ingested, failed = ingest_all_docs(docs_path, db)
        end_time = datetime.utcnow()

        duration = (end_time - start_time).total_seconds()
        logger.info(f"Ingestion completed in {duration:.2f} seconds")

        # Return exit code
        return 0 if failed == 0 else 1

    except Exception as e:
        logger.error(f"Ingestion failed: {e}")
        return 1

    finally:
        db.close()


if __name__ == '__main__':
    exit(main())
