import pandas as pd

class CatalogStats:
    @staticmethod
    def generate_summary(df: pd.DataFrame) -> dict:
        if df.empty:
            return {}
        
        return {
            "total_products": int(len(df)),
            "average_price": round(float(df["price"].mean()), 2),
            "min_price": round(float(df["price"].min()), 2),
            "max_price": round(float(df["price"].max()), 2),
            "most_common_rating": float(df["rating"].mode()[0]) if not df["rating"].empty else None,
            "available_count": int(df[df["availability"].str.contains("In Stock", case=False, na=False)].shape[0]),
            "highest_rated_products": df.nlargest(3, "rating")[["name", "rating", "price"]].to_dict(orient="records"),
            "lowest_priced_products": df.nsmallest(3, "price")[["name", "price"]].to_dict(orient="records")
        }