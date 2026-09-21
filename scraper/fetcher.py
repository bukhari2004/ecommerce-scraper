import json
import logging
import requests
from typing import Dict, Any, Optional
import config

logger = logging.getLogger(__name__)

class APIFetcher:
    def __init__(self, headers: Optional[Dict[str, str]] = None):
        self.headers = headers or config.DEFAULT_HEADERS
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def fetch_all_products(self) -> Dict[str, Any]:
        """Fetches product catalog via GET."""
        try:
            response = self.session.get(config.PRODUCTS_LIST_URL, timeout=config.REQUEST_TIMEOUT)
            response.raise_for_status()
            # Handle possible string-wrapped JSON responses from the endpoint
            data = response.json() if isinstance(response.json(), dict) else json.loads(response.text)
            return data
        except requests.RequestException as exc:
            logger.error("Error fetching products: %s", exc)
            return {"responseCode": 500, "products": []}

    def search_products(self, query: str) -> Dict[str, Any]:
        """Searches products via POST."""
        try:
            payload = {"search_product": query}
            response = self.session.post(config.SEARCH_PRODUCT_URL, data=payload, timeout=config.REQUEST_TIMEOUT)
            response.raise_for_status()
            data = response.json() if isinstance(response.json(), dict) else json.loads(response.text)
            return data
        except requests.RequestException as exc:
            logger.error("Error searching products for '%s': %s", query, exc)
            return {"responseCode": 500, "products": []}