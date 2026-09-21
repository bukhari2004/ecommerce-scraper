from flask import Flask, render_template, request, send_file, jsonify
import io
import pandas as pd
from scraper.fetcher import APIFetcher
from scraper.parser import ProductParser
from processing.transformer import DataTransformer
from storage.exporter import DataExporter

app = Flask(__name__)
fetcher = APIFetcher()

# In-memory storage for the latest search results
CURRENT_RESULTS = []

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/search", methods=["POST"])
def search():
    global CURRENT_RESULTS
    query = request.form.get("query", "").strip()

    if query:
        response_data = fetcher.search_products(query)
    else:
        response_data = fetcher.fetch_all_products()

    raw_items = ProductParser.parse_api_response(response_data)
    cleaned_items = DataTransformer.transform(raw_items)
    CURRENT_RESULTS = [item.model_dump() for item in cleaned_items]

    return jsonify({"success": True, "count": len(CURRENT_RESULTS), "products": CURRENT_RESULTS})

@app.route("/export/csv", methods=["GET"])
def export_csv():
    if not CURRENT_RESULTS:
        return "No data to export", 400
    df = pd.DataFrame(CURRENT_RESULTS)
    output = io.BytesIO()
    df.to_csv(output, index=False)
    output.seek(0)
    return send_file(output, mimetype="text/csv", as_attachment=True, download_name="clothing_search.csv")

@app.route("/export/excel", methods=["GET"])
def export_excel():
    if not CURRENT_RESULTS:
        return "No data to export", 400
    df = pd.DataFrame(CURRENT_RESULTS)
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Clothing")
    output.seek(0)
    return send_file(output, mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", as_attachment=True, download_name="clothing_search.xlsx")

if __name__ == "__main__":
    app.run(debug=True, port=5000)