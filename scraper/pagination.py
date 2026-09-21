import time
import requests
import logging
from bs4 import BeautifulSoup
from scraper.parser import ProductParser

logger = logging.getLogger(__name__)

class Paginator:
    @staticmethod
    def scrape_all_catalog(base_url: str = "https://automationexercise.com/products", max_pages: int = 2):
        """Iterates through paginated pages and respects request rates."""
        all_products = []
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        
        # AutomationExercise lists products on /products and supports search query pagination
        page_urls = [base_url]

        for idx, url in enumerate(page_urls, start=1):
            logger.info("Scraping page %d: %s", idx, url)
            try:
                res = requests.get(url, headers=headers, timeout=15)
                if res.status_code == 200:
                    products = ProductParser.parse_listing_page(res.text)
                    all_products.extend(products)
                time.sleep(1.0) # Polite delay
            except requests.RequestException as e:
                logger.error("Error scraping %s: %s", url, e)
                continue

        return all_products