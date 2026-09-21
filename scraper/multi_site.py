"""
scraper/multi_site.py
------------------------
Searches for a product across one or more configured website "profiles"
(see SITE_PROFILES in config.py) and returns a combined, tagged list of
Product records.

Two search strategies are supported per-site:
  - "live_search":  hits the site's real search URL directly.
  - "crawl_filter":  walks the site's paginated catalogue and keeps only
                      products whose name matches the search term. Used for
                      demo sites (like books.toscrape.com) that don't have
                      working search.

Every site is independent: if one site fails or times out, the others still
run and the failure is logged, not fatal.
"""

import logging
from urllib.parse import quote_plus, urljoin

from bs4 import BeautifulSoup

from config import SITE_PROFILES, MAX_PAGES
from scraper.fetcher import fetch_page, is_scraping_allowed
from scraper.models import Product

logger = logging.getLogger("scraper.multi_site")

RATING_WORDS = {"One": "1", "Two": "2", "Three": "3", "Four": "4", "Five": "5"}


def _extract_field(card, selector, attr=None):
    """Generic single-field extractor: returns None on any failure rather than raising."""
    if not selector:
        return None
    try:
        tag = card.select_one(selector)
        if not tag:
            return None
        if attr:
            return tag.get(attr, "").strip() or None
        return tag.get_text(strip=True)
    except Exception:
        return None


def _card_to_product(card, profile: dict, page_url: str, source_key: str) -> Product | None:
    product = Product(source_site=profile.get("display_name", source_key))

    product.name = _extract_field(card, profile.get("name_selector"), profile.get("name_attr"))
    product.price = _extract_field(card, profile.get("price_selector"))
    product.availability = _extract_field(card, profile.get("availability_selector"))

    rating_selector = profile.get("rating_selector")
    if rating_selector:
        try:
            tag = card.select_one(rating_selector)
            if tag:
                classes = tag.get("class", [])
                word = next((c for c in classes if c in RATING_WORDS), None)
                product.rating = word
        except Exception:
            pass

    link_selector = profile.get("link_selector")
    try:
        link_tag = card.select_one(link_selector) if link_selector else None
        if link_tag and link_tag.get("href"):
            product.url = urljoin(page_url, link_tag["href"])
    except Exception:
        pass

    if not product.name and not product.url:
        return None
    return product


def _search_live(session, key: str, profile: dict, query: str) -> list[Product]:
    search_url = profile["search_url_template"].format(query=quote_plus(query))
    logger.info("[%s] live search: %s", key, search_url)

    html = fetch_page(session, search_url)
    if html is None:
        logger.error("[%s] search request failed, skipping this site", key)
        return []

    soup = BeautifulSoup(html, "html.parser")
    cards = soup.select(profile["card_selector"])
    results = []
    for card in cards:
        product = _card_to_product(card, profile, search_url, key)
        if product:
            results.append(product)

    logger.info("[%s] found %d result(s)", key, len(results))
    return results


def _search_crawl_filter(session, key: str, profile: dict, query: str, max_pages: int) -> list[Product]:
    query_lower = query.lower()
    matches: list[Product] = []
    page = 1

    while page <= max_pages:
        page_url = profile["listing_url_template"].format(page=page)
        html = fetch_page(session, page_url)
        if html is None:
            logger.warning("[%s] could not fetch page %d, stopping crawl for this site", key, page)
            break

        soup = BeautifulSoup(html, "html.parser")
        cards = soup.select(profile["card_selector"])
        if not cards:
            break

        for card in cards:
            product = _card_to_product(card, profile, page_url, key)
            if product and product.name and query_lower in product.name.lower():
                matches.append(product)

        next_selector = profile.get("next_page_selector")
        has_next = bool(next_selector and soup.select_one(next_selector))
        if not has_next:
            break
        page += 1

    logger.info("[%s] scanned %d page(s), found %d match(es)", key, page, len(matches))
    return matches


def search_site(session, key: str, query: str, max_pages: int = MAX_PAGES) -> list[Product]:
    """Search a single configured site by its profile key. Never raises."""
    profile = SITE_PROFILES.get(key)
    if not profile:
        logger.error("Unknown site profile key: %s", key)
        return []

    if not is_scraping_allowed(profile["base_url"]):
        logger.error("[%s] robots.txt disallows scraping. Skipping this site.", key)
        return []

    try:
        if profile["mode"] == "live_search":
            return _search_live(session, key, profile, query)
        elif profile["mode"] == "crawl_filter":
            return _search_crawl_filter(session, key, profile, query, max_pages)
        else:
            logger.error("[%s] unknown mode: %s", key, profile.get("mode"))
            return []
    except Exception as exc:
        logger.error("[%s] unexpected error during search: %s", key, exc)
        return []


def search_all_sites(session, keys: list[str], query: str, max_pages: int = MAX_PAGES) -> list[Product]:
    """Search every given site key for the query and return the combined results."""
    all_results: list[Product] = []
    for key in keys:
        all_results.extend(search_site(session, key, query, max_pages))
    logger.info("Combined search complete: %d total result(s) across %d site(s)", len(all_results), len(keys))
    return all_results
