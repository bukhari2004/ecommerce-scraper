import re

class DataCleaner:
    @staticmethod
    def clean_price(price_val) -> int:
        if price_val is None:
            return 0
        
        # If already an integer or float, convert directly
        if isinstance(price_val, (int, float)):
            return int(price_val)
        
        val_str = str(price_val).strip()
        
        # Extract ONLY digits (e.g., from "Rs. 1000" or "Rs. 478" -> "1000", "478")
        digits = re.findall(r"\d+", val_str)
        if digits:
            # Join all digit groups to handle formatted numbers like "1,000"
            return int("".join(digits))
            
        return 0

    @staticmethod
    def clean_text(text: str) -> str:
        return text.strip() if text else "Unknown"