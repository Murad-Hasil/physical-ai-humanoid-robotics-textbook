"""
T053 — Batch Curriculum Ingestion CLI Script

Reads the Docusaurus docs folder structure and ingests all 13 weeks
into the backend via POST /api/v1/curriculum/ingest.

PDF-defined curriculum structure:
  Weeks 1-2  : Introduction to Physical AI  (foundation/)
  Weeks 3-5  : ROS 2 Fundamentals           (01-ros-2/)
  Weeks 6-7  : Robot Simulation with Gazebo (02-gazebo/)
  Weeks 8-10 : NVIDIA Isaac Platform        (03-nvidia-isaac/)
  Weeks 11-12: Humanoid Robot Development   (04-humanoid/)
  Week 13    : Conversational Robotics      (04-humanoid/week-13-...)

Usage:
    python ingest_curriculum.py --content-path ../docusaurus-textbook/docs \\
                                --api-url http://localhost:8000 \\
                                --token <jwt_token>

    # With summary regeneration:
    python ingest_curriculum.py --content-path ../docusaurus-textbook/docs \\
                                --api-url http://localhost:8000 \\
                                --token <jwt_token> \\
                                --regenerate-summaries

    # Ingest specific weeks only:
    python ingest_curriculum.py --content-path ../docusaurus-textbook/docs \\
                                --api-url http://localhost:8000 \\
                                --token <jwt_token> \\
                                --weeks 1 2 3
"""

import argparse
import json
import logging
import re
import sys
from pathlib import Path

import requests

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("ingest_curriculum")


# ---------------------------------------------------------------------------
# Week number → folder mapping (derived from PDF curriculum)
# ---------------------------------------------------------------------------

# Each entry maps a week number to the folder that contains that week's file
# and the markdown filename inside that folder.
WEEK_MAP: dict[int, dict] = {
    1:  {"folder": "foundation",     "file": "week-01-introduction-to-physical-ai.md",  "module": "Introduction to Physical AI"},
    2:  {"folder": "foundation",     "file": "week-02-physical-ai-architecture.md",      "module": "Introduction to Physical AI"},
    3:  {"folder": "01-ros-2",       "file": "week-03-introduction-to-ros-2.md",         "module": "ROS 2 Fundamentals"},
    4:  {"folder": "01-ros-2",       "file": "week-04-ros-2-nodes-and-topics.md",        "module": "ROS 2 Fundamentals"},
    5:  {"folder": "01-ros-2",       "file": "week-05-ros-2-services-and-actions.md",    "module": "ROS 2 Fundamentals"},
    6:  {"folder": "02-gazebo",      "file": "week-06-introduction-to-gazebo.md",        "module": "Robot Simulation with Gazebo"},
    7:  {"folder": "02-gazebo",      "file": "week-07-robot-modeling-in-gazebo.md",      "module": "Robot Simulation with Gazebo"},
    8:  {"folder": "03-nvidia-isaac", "file": "week-08-introduction-to-isaac-sim.md",   "module": "NVIDIA Isaac Platform"},
    9:  {"folder": "03-nvidia-isaac", "file": "week-09-isaac-ros-integration.md",        "module": "NVIDIA Isaac Platform"},
    10: {"folder": "03-nvidia-isaac", "file": "week-10-perception-models.md",            "module": "NVIDIA Isaac Platform"},
    11: {"folder": "04-humanoid",    "file": "week-11-humanoid-robot-basics.md",         "module": "Humanoid Robot Development"},
    12: {"folder": "04-humanoid",    "file": "week-12-conversational-ai-integration.md", "module": "Humanoid Robot Development"},
    13: {"folder": "04-humanoid",    "file": "week-13-complete-humanoid-system.md",      "module": "Conversational Robotics"},
}


# ---------------------------------------------------------------------------
# Markdown frontmatter parser
# ---------------------------------------------------------------------------

def parse_frontmatter(content: str) -> tuple[dict, str]:
    """
    Extract YAML frontmatter and body from markdown content.

    Returns:
        (metadata_dict, body_without_frontmatter)
    """
    meta: dict = {}
    body = content

    match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
    if match:
        frontmatter_text = match.group(1)
        for line in frontmatter_text.splitlines():
            if ":" in line:
                key, _, value = line.partition(":")
                meta[key.strip()] = value.strip().strip('"').strip("'")
        body = content[match.end():]

    return meta, body


# ---------------------------------------------------------------------------
# Week reader
# ---------------------------------------------------------------------------

def read_week(week_number: int, docs_path: Path) -> dict | None:
    """
    Read a single week's markdown file and return a WeekIngestRequest dict.

    Returns None if the file does not exist (logs a warning).
    """
    info = WEEK_MAP[week_number]
    md_path = docs_path / info["folder"] / info["file"]

    if not md_path.exists():
        logger.warning(f"Week {week_number:02d} — file not found: {md_path}")
        return None

    logger.info(f"Week {week_number:02d} — reading {md_path.relative_to(docs_path)}")

    raw = md_path.read_text(encoding="utf-8")
    meta, body = parse_frontmatter(raw)

    title = meta.get("title") or f"Week {week_number} — {info['module']}"
    description = meta.get("description") or info["module"]

    # One chapter per file (each .md = one chapter in this curriculum)
    chapter = {
        "title": title,
        "content": body.strip(),
        "order": 1,
        "estimated_time": meta.get("estimated_time", "3-4 hours"),
        "tags": [info["module"].lower().replace(" ", "-"), f"week-{week_number}"],
        "hardware_relevant": ["sim_rig", "edge_kit"],
    }

    return {
        "week_number": week_number,
        "title": title,
        "description": description,
        "chapters": [chapter],
    }


# ---------------------------------------------------------------------------
# API caller
# ---------------------------------------------------------------------------

def ingest_weeks(
    weeks_data: list[dict],
    api_url: str,
    token: str,
    regenerate_summaries: bool,
) -> dict:
    """
    POST weeks_data to /api/v1/curriculum/ingest.

    Returns parsed JSON response.
    Raises requests.HTTPError on non-2xx status.
    """
    url = f"{api_url.rstrip('/')}/api/v1/curriculum/ingest"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    # Backend accepts list of WeekIngestRequest directly as request body
    payload = weeks_data

    logger.info(f"POST {url}  ({len(weeks_data)} weeks, regenerate_summaries={regenerate_summaries})")

    response = requests.post(url, headers=headers, json=payload, timeout=120)
    response.raise_for_status()
    return response.json()


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Batch-ingest the 13-week Physical AI curriculum into the backend.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--content-path",
        required=True,
        help="Path to the Docusaurus docs/ folder containing week markdown files.",
    )
    parser.add_argument(
        "--api-url",
        default="http://localhost:8000",
        help="Backend API base URL (default: http://localhost:8000)",
    )
    parser.add_argument(
        "--token",
        required=True,
        help="JWT access token for an admin user.",
    )
    parser.add_argument(
        "--regenerate-summaries",
        action="store_true",
        default=False,
        help="Trigger AI summary regeneration for ingested chapters.",
    )
    parser.add_argument(
        "--weeks",
        nargs="+",
        type=int,
        metavar="N",
        help="Ingest only specific week numbers (e.g. --weeks 1 2 3). Default: all 13.",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=13,
        help="How many weeks to send per API request (default: 13 = all at once).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=False,
        help="Parse files and print payload without calling the API.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    docs_path = Path(args.content_path).resolve()
    if not docs_path.is_dir():
        logger.error(f"content-path does not exist or is not a directory: {docs_path}")
        return 1

    # Determine which weeks to process
    week_numbers = sorted(args.weeks or list(WEEK_MAP.keys()))
    invalid = [w for w in week_numbers if w not in WEEK_MAP]
    if invalid:
        logger.error(f"Invalid week numbers: {invalid}. Valid range: 1-13.")
        return 1

    logger.info(f"docs path  : {docs_path}")
    logger.info(f"api url    : {args.api_url}")
    logger.info(f"weeks      : {week_numbers}")
    logger.info(f"regen summ : {args.regenerate_summaries}")
    logger.info(f"dry run    : {args.dry_run}")
    logger.info("-" * 60)

    # Read all requested weeks
    weeks_data: list[dict] = []
    skipped: list[int] = []

    for wn in week_numbers:
        week = read_week(wn, docs_path)
        if week:
            weeks_data.append(week)
        else:
            skipped.append(wn)

    if not weeks_data:
        logger.error("No valid week files found. Nothing to ingest.")
        return 1

    if skipped:
        logger.warning(f"Skipped weeks (files missing): {skipped}")

    logger.info(f"\nReady to ingest {len(weeks_data)} weeks.")

    if args.dry_run:
        logger.info("DRY RUN — printing payload:")
        print(json.dumps(weeks_data, indent=2, ensure_ascii=False))
        return 0

    # Send in batches
    batch_size = max(1, args.batch_size)
    total_ingested = 0

    for i in range(0, len(weeks_data), batch_size):
        batch = weeks_data[i : i + batch_size]
        batch_week_nums = [w["week_number"] for w in batch]
        logger.info(f"Sending batch {i // batch_size + 1}: weeks {batch_week_nums}")

        try:
            result = ingest_weeks(batch, args.api_url, args.token, args.regenerate_summaries)
            ingested = result.get("weeks_ingested", len(batch))
            total_ingested += ingested
            logger.info(f"  ✓ Batch complete — {ingested} weeks ingested")
        except requests.HTTPError as exc:
            logger.error(f"  ✗ HTTP error: {exc.response.status_code} — {exc.response.text}")
            return 1
        except requests.ConnectionError:
            logger.error(f"  ✗ Cannot connect to {args.api_url}. Is the backend running?")
            return 1
        except Exception as exc:
            logger.error(f"  ✗ Unexpected error: {exc}")
            return 1

    logger.info("-" * 60)
    logger.info(f"Ingestion complete — {total_ingested}/{len(weeks_data)} weeks ingested successfully.")

    if skipped:
        logger.warning(f"Weeks not ingested (missing files): {skipped}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
