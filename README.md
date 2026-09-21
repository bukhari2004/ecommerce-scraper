# E-Commerce Product Data Web Scraper

A modular Python pipeline that scrapes product data, cleans and validates it,
exports it to CSV/Excel, and produces summary statistics and charts.

## ⚠️ A note on target sites

This project defaults to **[books.toscrape.com](https://books.toscrape.com)**,
a site built specifically for practicing web scraping — its `robots.txt`
allows it and its HTML structure is stable.

Large marketplaces (Amazon, Alibaba, Daraz, etc.) **prohibit automated
scraping in their Terms of Service** and run active anti-bot defenses. Do not
point this scraper at them. If you need real product data from those
platforms, use their official developer/partner APIs instead:

- Amazon Product Advertising API
- Alibaba Open Platform
- Daraz Open Platform

Swapping this project to a different *scraping-permitted* site only requires
editing `config.py` and the CSS selectors in `scraper/parser.py`.

## Project structure

```
web-scraping-project/
├── scraper/          # fetching, parsing, pagination, data model
├── processing/        # cleaning, transforming, validating
├── storage/            # CSV / Excel export
├── analysis/           # summary stats + matplotlib charts
├── data/               # raw scraped JSON snapshot
├── output/              # final CSV, XLSX, and PNG charts
├── notebooks/            # exploratory analysis notebook
├── logs/                  # scraper.log
├── config.py
├── main.py
└── requirements.txt
```

## Setup

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

**Full catalogue scrape** (scrapes the entire demo book catalogue):
```bash
python main.py                    # full run
python main.py --max-pages 5      # quick test on first 5 pages
python main.py --no-details       # skip per-product detail pages (faster, no category/description)
```

**Multi-site product search** (searches one product name across configured sites):
```bash
python main.py --search "charizard"                     # uses config.DEFAULT_SEARCH_SITES
python main.py --search "charizard" --sites books,scrapeme
```
This mode does NOT crawl a whole catalogue — for sites with real search
(`mode: "live_search"` in `config.SITE_PROFILES`) it hits the search URL
directly; for demo sites with no search (`mode: "crawl_filter"`) it walks
the catalogue and keeps only name matches. Results from every site are
combined into one table with a **Source Site** column, in the CSV, Excel
file, and the dashboard (filterable by site).

Add `--no-browser` to either mode to skip auto-opening the dashboard.

## Configured sites

Three real, live websites are configured out of the box — all explicitly
permit automated access for learning/practice purposes:

| Key | Site | Search mode |
|---|---|---|
| `books` | books.toscrape.com | crawls & filters (no live search on that site) |
| `scrapeme` | scrapeme.live (Pokémon shop) | live search (`?s=`) |
| `webscrapingdev` | web-scraping.dev | crawls & filters (small catalog, ~28 products) |

Run `python main.py --search "term"` (or use the live dashboard, `python
app.py`) and it checks all three by default.

## Live search dashboard (type-and-search in the browser)

For a page where you type a product name and click Search — with the
scraping happening live, no terminal commands needed after startup — run:

```bash
python app.py
```

Then open **http://127.0.0.1:5000** in your browser. Type a product name,
tick which sites to check, and click Search. Results appear on the page
with an Export CSV / Export Excel button. Press `CTRL+C` in the terminal
to stop the server when you're done.

This is a local development server for personal use — it is not meant to
be exposed to the internet.

Outputs:
- `output/products_clean.csv`
- `output/products_clean.xlsx`
- `output/dashboard.html` — searchable/sortable browser dashboard (auto-opens)
- `output/price_distribution.png`
- `output/rating_distribution.png`
- `output/price_vs_rating.png`
- `output/products_by_category.png`
- `logs/scraper.log`

## Pipeline stages

1. **robots.txt check** — aborts if disallowed.
2. **Scrape** — paginated listing pages + optional detail-page visits, with
   retries/backoff and a politeness delay between requests.
3. **Clean** — dedupes by URL, normalizes names, fills missing values.
4. **Transform** — parses price strings to floats, standardizes ratings to
   a 0–5 numeric scale.
5. **Validate** — drops records missing required fields or with out-of-range
   values.
6. **Export** — CSV and Excel with clean, labeled columns.
7. **Analyze** — totals, average/min/max price, most common rating,
   available-product count, top-rated and lowest-priced products.
8. **Visualize** — 4 charts saved as PNGs.

## Extending to a new site

**For the full catalogue scraper:**
1. Update `BASE_URL` / `PAGE_URL_TEMPLATE` in `config.py`.
2. Update the CSS selectors in `scraper/parser.py` to match the new site's
   HTML.
3. Re-check `robots.txt` — the pipeline verifies this automatically at
   startup and will refuse to run if disallowed.

**For multi-site search (`--search`):**
Add a new entry to `SITE_PROFILES` in `config.py`. Right-click on the target
site in your browser, choose "Inspect", and find:
- the CSS selector wrapping one product card (`card_selector`)
- the selector for the product name inside a card (`name_selector`)
- the selector for the price (`price_selector`)
- the link to the product (`link_selector`)

If the site has a working search box, set `"mode": "live_search"` and fill
in `search_url_template` (must contain `{query}`). If it doesn't, use
`"mode": "crawl_filter"` with a `listing_url_template` and
`next_page_selector`, and the scraper will crawl the catalogue and filter
by name instead — only practical on small demo catalogues.

The robots.txt check runs automatically for every site profile before it's
scraped, so a disallowed site is skipped (not scraped) rather than causing
an error.
