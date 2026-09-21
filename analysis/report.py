"""
analysis/report.py
--------------------
Builds a single self-contained HTML dashboard (summary cards, searchable
product table, and the four charts) from the cleaned dataset, and opens
it in the user's default web browser.

No external dependencies beyond what's already in requirements.txt —
the table search/sort is plain vanilla JavaScript, no CDN needed.
"""

import json
import logging
import os
import webbrowser

import pandas as pd

logger = logging.getLogger("analysis.report")

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Product Scrape Dashboard</title>
<style>
  :root {{
    --bg: #0f1117; --card: #1a1d27; --border: #2a2e3a;
    --text: #e8e9ed; --muted: #9aa0ae; --accent: #6c8eff;
  }}
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0; padding: 32px; background: var(--bg); color: var(--text);
    font-family: -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif;
  }}
  h1 {{ margin: 0 0 4px 0; font-size: 26px; }}
  .subtitle {{ color: var(--muted); margin-bottom: 28px; font-size: 14px; }}
  .cards {{
    display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
    gap: 14px; margin-bottom: 32px;
  }}
  .card {{
    background: var(--card); border: 1px solid var(--border); border-radius: 10px;
    padding: 16px 18px;
  }}
  .card .label {{ color: var(--muted); font-size: 12px; text-transform: uppercase; letter-spacing: .04em; }}
  .card .value {{ font-size: 24px; font-weight: 600; margin-top: 6px; }}
  .section-title {{ font-size: 18px; font-weight: 600; margin: 36px 0 14px 0; }}
  .charts {{
    display: grid; grid-template-columns: repeat(auto-fit, minmax(360px, 1fr));
    gap: 16px; margin-bottom: 32px;
  }}
  .charts img {{
    width: 100%; border-radius: 10px; border: 1px solid var(--border); background: #fff;
  }}
  .controls {{ display: flex; gap: 10px; margin-bottom: 14px; flex-wrap: wrap; }}
  input[type=text], select {{
    background: var(--card); border: 1px solid var(--border); color: var(--text);
    padding: 9px 12px; border-radius: 8px; font-size: 14px;
  }}
  input[type=text] {{ flex: 1; min-width: 220px; }}
  table {{ width: 100%; border-collapse: collapse; background: var(--card); border-radius: 10px; overflow: hidden; }}
  th, td {{ text-align: left; padding: 10px 12px; border-bottom: 1px solid var(--border); font-size: 13px; }}
  th {{ background: #20232f; cursor: pointer; user-select: none; color: var(--muted); font-weight: 600; }}
  th:hover {{ color: var(--text); }}
  tr:hover td {{ background: #1f2330; }}
  a {{ color: var(--accent); text-decoration: none; }}
  a:hover {{ text-decoration: underline; }}
  .rowcount {{ color: var(--muted); font-size: 13px; margin: 10px 0; }}
</style>
</head>
<body>

<h1>Product Scrape Dashboard</h1>
<div class="subtitle">Generated from products_clean.csv &middot; {total} products</div>

<div class="cards">
  <div class="card"><div class="label">Total Products</div><div class="value">{total}</div></div>
  <div class="card"><div class="label">Average Price</div><div class="value">{avg_price}</div></div>
  <div class="card"><div class="label">Price Range</div><div class="value">{min_price} &ndash; {max_price}</div></div>
  <div class="card"><div class="label">Most Common Rating</div><div class="value">{common_rating} / 5</div></div>
  <div class="card"><div class="label">In Stock</div><div class="value">{available}</div></div>
</div>

<div class="section-title">Charts</div>
<div class="charts">
  {chart_tags}
</div>

<div class="section-title">Product Data</div>
<div class="controls">
  <input type="text" id="searchBox" placeholder="Search by name or category...">
  <select id="categoryFilter"><option value="">All categories</option>{category_options}</select>
  <select id="siteFilter"><option value="">All sites</option>{site_options}</select>
</div>
<div class="rowcount" id="rowCount"></div>
<table id="productTable">
  <thead>
    <tr>
      <th data-key="source_site">Site</th>
      <th data-key="name">Name</th>
      <th data-key="price">Price</th>
      <th data-key="rating">Rating</th>
      <th data-key="availability">Availability</th>
      <th data-key="category">Category</th>
    </tr>
  </thead>
  <tbody id="tableBody"></tbody>
</table>

<script>
const products = {products_json};

const tbody = document.getElementById('tableBody');
const searchBox = document.getElementById('searchBox');
const categoryFilter = document.getElementById('categoryFilter');
const siteFilter = document.getElementById('siteFilter');
const rowCount = document.getElementById('rowCount');
let sortKey = null, sortAsc = true;

function render() {{
  const term = searchBox.value.toLowerCase();
  const cat = categoryFilter.value;
  const site = siteFilter.value;
  let rows = products.filter(p =>
    (!term || (p.name || '').toLowerCase().includes(term) || (p.category || '').toLowerCase().includes(term)) &&
    (!cat || p.category === cat) &&
    (!site || p.source_site === site)
  );
  if (sortKey) {{
    rows.sort((a, b) => {{
      let av = a[sortKey], bv = b[sortKey];
      if (sortKey === 'price' || sortKey === 'rating') {{ av = parseFloat(av) || 0; bv = parseFloat(bv) || 0; }}
      if (av < bv) return sortAsc ? -1 : 1;
      if (av > bv) return sortAsc ? 1 : -1;
      return 0;
    }});
  }}
  rowCount.textContent = rows.length + ' product(s) shown';
  tbody.innerHTML = rows.map(p => `
    <tr>
      <td>${{p.source_site || ''}}</td>
      <td><a href="${{p.url || '#'}}" target="_blank">${{p.name || ''}}</a></td>
      <td>${{p.price || ''}}</td>
      <td>${{p.rating_numeric != null ? p.rating_numeric + ' / 5' : ''}}</td>
      <td>${{p.availability || ''}}</td>
      <td>${{p.category || ''}}</td>
    </tr>
  `).join('');
}}

searchBox.addEventListener('input', render);
categoryFilter.addEventListener('change', render);
siteFilter.addEventListener('change', render);
document.querySelectorAll('th[data-key]').forEach(th => {{
  th.addEventListener('click', () => {{
    const key = th.dataset.key;
    if (sortKey === key) sortAsc = !sortAsc; else {{ sortKey = key; sortAsc = true; }}
    render();
  }});
}});

render();
</script>

</body>
</html>
"""


def generate_html_report(df: pd.DataFrame, summary: dict, output_dir: str, open_browser: bool = True) -> str:
    """
    Build dashboard.html in output_dir from the cleaned dataframe + summary
    stats, embedding the previously-generated chart PNGs. Returns the path
    written. If open_browser is True, opens it in the default browser.
    """
    records = df.rename(columns={"rating_numeric": "rating_numeric"}).to_dict(orient="records")
    # Keep only the fields the dashboard needs, JSON-safe (NaN -> None)
    clean_records = []
    for r in records:
        clean_records.append({
            "name": r.get("name"),
            "price": r.get("price"),
            "rating_numeric": None if pd.isna(r.get("rating_numeric")) else r.get("rating_numeric"),
            "availability": r.get("availability"),
            "category": r.get("category"),
            "url": r.get("url"),
            "source_site": r.get("source_site"),
        })

    categories = sorted({r["category"] for r in clean_records if r["category"]})
    category_options = "".join(f'<option value="{c}">{c}</option>' for c in categories)

    sites = sorted({r["source_site"] for r in clean_records if r["source_site"]})
    site_options = "".join(f'<option value="{s}">{s}</option>' for s in sites)

    chart_files = [
        ("price_distribution.png", "Price Distribution"),
        ("rating_distribution.png", "Rating Distribution"),
        ("price_vs_rating.png", "Price vs Rating"),
        ("products_by_category.png", "Products by Category"),
    ]
    chart_tags = "".join(
        f'<img src="{fname}" alt="{label}">'
        for fname, label in chart_files
        if os.path.exists(os.path.join(output_dir, fname))
    )

    html = TEMPLATE.format(
        total=summary.get("total_products", 0),
        avg_price=summary.get("average_price", "N/A"),
        min_price=summary.get("min_price", "N/A"),
        max_price=summary.get("max_price", "N/A"),
        common_rating=summary.get("most_common_rating", "N/A"),
        available=summary.get("available_products", "N/A"),
        chart_tags=chart_tags,
        category_options=category_options,
        site_options=site_options,
        products_json=json.dumps(clean_records),
    )

    report_path = os.path.join(output_dir, "dashboard.html")
    os.makedirs(output_dir, exist_ok=True)
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(html)
    logger.info("Wrote dashboard: %s", report_path)

    if open_browser:
        try:
            webbrowser.open(f"file://{os.path.abspath(report_path)}")
        except Exception as exc:
            logger.warning("Could not auto-open browser: %s", exc)

    return report_path
