import pandas as pd
from typing import List
from scraper.models import CleanedProduct
import config

class DataExporter:
    @staticmethod
    def to_dataframe(items: List[CleanedProduct]) -> pd.DataFrame:
        return pd.DataFrame([item.model_dump() for item in items])

    @classmethod
    def export_all(cls, items: List[CleanedProduct], base_name: str = "clothing_products") -> dict:
        df = cls.to_dataframe(items)
        
        csv_path = config.DATA_DIR / f"{base_name}.csv"
        excel_path = config.DATA_DIR / f"{base_name}.xlsx"

        # CSV Export
        df.to_csv(csv_path, index=False)
        
        # Excel Export with formatting
        with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="Products")

        return {"csv": str(csv_path), "excel": str(excel_path)}