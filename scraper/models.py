from pydantic import BaseModel
from typing import Optional

class RawProduct(BaseModel):
    id: Optional[int] = None
    name: str
    price: str
    rating: Optional[float] = 4.0  # Default or scraped rating
    availability: Optional[str] = "In Stock"
    category: Optional[str] = "General"
    brand: Optional[str] = "Unbranded"
    description: Optional[str] = ""
    product_url: str
    image_url: Optional[str] = ""

class CleanedProduct(BaseModel):
    product_id: int
    name: str
    price: float
    rating: float
    availability: str
    category: str
    brand: str
    description: str
    product_url: str
    image_url: str