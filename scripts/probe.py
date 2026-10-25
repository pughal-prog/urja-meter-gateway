"""Manual read-only portal exploration probe.

This script allows polite, interactive testing of single endpoints during investigation
without launching the full web service.
"""

import asyncio
import logging
import sys
from pathlib import Path

# Add src to sys.path to enable execution without prior pip install
src_dir = Path(__file__).resolve().parent.parent / "src"
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

from urja_api.config import get_settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("probe")


async def main() -> None:
    settings = get_settings()
    logger.info("Initializing probe for portal: %s", settings.portal_base_url)
    # Placeholder for read-only test calls during Phase 1 investigation
    logger.info("Probe initialized in read-only mode.")


if __name__ == "__main__":
    asyncio.run(main())
