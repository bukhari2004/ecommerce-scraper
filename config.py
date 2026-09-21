from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"
LOGS_DIR = BASE_DIR / "logs"

for folder in [DATA_DIR, OUTPUT_DIR, LOGS_DIR]:
    folder.mkdir(parents=True, exist_ok=True)

# AutomationExercise API Endpoints
API_BASE_URL = "https://automationexercise.com/api"
PRODUCTS_LIST_URL = f"{API_BASE_URL}/productsList"
SEARCH_PRODUCT_URL = f"{API_BASE_URL}/searchProduct"

REQUEST_TIMEOUT = 15
DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}