# E-Commerce Product Data Web Scraper & Dashboard

A modular end-to-end Python pipeline that extracts real-time product data from the [AutomationExercise](https://automationexercise.com) e-commerce catalog, cleans and validates the dataset, exports to CSV/Excel, and provides an interactive web dashboard and exploratory data analysis (EDA) notebook.

---
## 🌐 Live Application
- **Live Demo**: [https://ecommerce-scraper-nine.vercel.app/](https://ecommerce-scraper-nine.vercel.app/)
- **Repository**: https://github.com/bukhari2004/ecommerce-scraper
## Features

- **Automated Data Extraction:** Fetches full product listings including titles, prices, brands, categories, thumbnail images, and store URLs.
- **Data Cleaning & Normalization:** Robust regex-based price cleaning and category restructuring with Pydantic schema validation.
- **Multi-Format Export:** Automatically saves validated records to CSV and Excel (`data/clothing_products.csv` and `data/clothing_products.xlsx`).
- **Exploratory Data Analysis (EDA):** Jupyter notebook (`notebooks/eda.ipynb`) with visual price distributions, brand rankings, and statistical summaries.
- **Interactive Web Dashboard:** Clean, responsive Flask interface (`app.py`) featuring real-time keyword search, image thumbnails, store redirect links, and direct CSV/Excel download buttons.
- **One-Click Execution:** Windows batch script (`run_dashboard.bat`) to run the ETL pipeline and launch the dashboard in your browser with a single click.

---

## Project Structure

```text
web-scraping-project/
│
├── data/                      # Generated CSV and Excel datasets
│   ├── clothing_products.csv
│   └── clothing_products.xlsx
├── notebooks/                 # Jupyter Notebooks for analysis
│   └── eda.ipynb
├── output/                    # Generated charts and visualization images
│   └── price_dist.png
├── processing/                # Data cleaning and transformation pipeline
│   └── transformer.py
├── scraper/                   # Extraction logic and Pydantic schemas
│   ├── client.py
│   └── models.py
├── storage/                   # File writer modules (CSV & Excel)
│   └── exporter.py
├── templates/                 # Frontend dashboard HTML
│   └── index.html
├── .gitignore
├── app.py                     # Flask web dashboard application
├── config.py                  # Project settings and endpoints
├── main.py                    # Main pipeline runner (Scrape -> Clean -> Export)
├── requirements.txt           # Python dependencies
└── run_dashboard.bat          # 1-click Windows runner