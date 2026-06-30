"""Main scraper module for extracting Collembola species data."""

import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

DATA_DIR = Path(__file__).parent.parent / "data"
IMAGES_DIR = Path(__file__).parent.parent / "images"


def scrape():
    """Main scraping function. To be implemented."""
    logger.info("Scraping not yet implemented.")
    raise NotImplementedError("Scraper not yet implemented.")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    scrape()
