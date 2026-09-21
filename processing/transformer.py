from typing import List
from scraper.models import RawProduct, CleanedProduct
from processing.cleaner import DataCleaner

class DataTransformer:
    @staticmethod
    def transform(raw_products: List[RawProduct]) -> List[CleanedProduct]:
        transformed = []
        for p in raw_products:
            numeric_price = DataCleaner.clean_price(p.price)
            category_meta = p.category or {}
            usertype = category_meta.get("usertype", {}).get("usertype", "Unisex")
            sub_category = category_meta.get("category", "General")

            product_url = f"https://automationexercise.com/product_details/{p.id}"
            image_url = f"https://automationexercise.com/get_product_picture/{p.id}"

            transformed.append(
                CleanedProduct(
                    product_id=p.id,
                    title=DataCleaner.clean_text(p.name),
                    price_inr=numeric_price,
                    brand=DataCleaner.clean_text(p.brand) if p.brand else "Unbranded",
                    user_type=usertype,
                    category=sub_category,
                    image_url=image_url,
                    product_url=product_url
                )
            )
        return transformed