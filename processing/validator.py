from typing import List
from scraper.models import CleanedProduct
import logging

logger = logging.getLogger(__name__)

class DataValidator:
    @staticmethod
    def validate_and_deduplicate(items: List[CleanedProduct]) -> List[CleanedProduct]:
        seen_ids = set()
        valid_items = []

        for item in items:
            # Drop duplicates by ID
            if item.product_id in seen_ids:
                logger.warning("Duplicate product ID %d discarded.", item.product_id)
                continue
            
            # Validate essential fields
            if not item.name or item.name == "Unknown":
                continue
            if item.price < 0:
                continue

            seen_ids.add(item.product_id)
            valid_items.append(item)

        return valid_items