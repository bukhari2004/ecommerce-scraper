import logging
from scraper.pagination import Paginator
from processing.cleaner import DataCleaner
from processing.validator import DataValidator
from scraper.models import CleanedProduct
from storage.exporter import DataExporter
from analysis.stats import CatalogStats
from analysis.visualize import CatalogVisualizer

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("Scraper")

def main():
    logger.info("Executing Milestone Scraper Pipeline (BS4 + Requests)...")
    
    # 1. Scrape & Paginate
    raw_products = Paginator.scrape_all_catalog()
    logger.info("Scraped %d raw items from catalog HTML.", len(raw_products))

    # 2. Clean and Transform
    cleaned = []
    for p in raw_products:
        cleaned.append(
            CleanedProduct(
                product_id=p.id or 0,
                name=DataCleaner.clean_text(p.name),
                price=DataCleaner.clean_price(p.price),
                rating=p.rating or 4.0,
                availability=p.availability or "In Stock",
                category=p.category or "Apparel",
                brand=p.brand or "Generic",
                description=p.description or f"{p.name} in brand {p.brand}",
                product_url=p.product_url,
                image_url=p.image_url or ""
            )
        )

    # 3. Validate & Deduplicate
    valid_items = DataValidator.validate_and_deduplicate(cleaned)
    logger.info("Validated %d unique products.", len(valid_items))

    # 4. Export CSV and Excel
    paths = DataExporter.export_all(valid_items)
    logger.info("Saved CSV: %s", paths["csv"])
    logger.info("Saved Excel: %s", paths["excel"])

    # 5. Full Statistical Analysis
    df = DataExporter.to_dataframe(valid_items)
    stats = CatalogStats.generate_summary(df)
    
    print("\n" + "="*40)
    print("      SCRAPING & ANALYSIS SUMMARY      ")
    print("="*40)
    print(f"Total Products Scraped : {stats.get('total_products')}")
    print(f"Average Price          : Rs. {stats.get('average_price')}")
    print(f"Price Range            : Rs. {stats.get('min_price')} - Rs. {stats.get('max_price')}")
    print(f"Most Common Rating     : {stats.get('most_common_rating')} Stars")
    print(f"In-Stock Items         : {stats.get('available_count')}")
    print(f"Lowest Priced Products : {stats.get('lowest_priced_products')}")
    print("="*40 + "\n")

    # 6. Generate All 4 Required Visualizations
    chart_path = CatalogVisualizer.generate_all_plots(df)
    logger.info("Generated 4 required charts in: %s", chart_path)

if __name__ == "__main__":
    main()