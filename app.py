import logging
import requests
from flask import Flask, jsonify, render_template, request

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)  # <-- this line MUST exist before any @app.route


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/search", methods=["POST"])
def search():
    query = request.form.get("query", "").strip()
    if not query:
        return jsonify({"status": "success", "count": 0, "products": []})

    api_url = "https://automationexercise.com/api/searchProduct"
    try:
        response = requests.post(api_url, data={"search_product": query}, timeout=15)
        response.raise_for_status()
        data = response.json()
        raw_list = data.get("products", [])

        results = []
        for p in raw_list:
            cat_info = p.get("category") or {}
            cat_name = cat_info.get("category", "") if isinstance(cat_info, dict) else str(cat_info)
            user_type_obj = cat_info.get("usertype", {}) if isinstance(cat_info, dict) else {}
            user_type = user_type_obj.get("usertype", "") if isinstance(user_type_obj, dict) else str(user_type_obj)

            raw_price = str(p.get("price", "0"))
            clean_price = raw_price.replace("Rs.", "").strip()
            item_id = p.get("id", "")

            results.append({
                "id": item_id,
                "name": p.get("name", "Unnamed Item"),
                "price": clean_price,
                "brand": p.get("brand", "Unbranded"),
                "category": cat_name,
                "target": user_type or "General",
                # The API has NO image field — this is the real, working
                # image URL pattern the site itself uses per product id.
                "image": f"https://automationexercise.com/get_product_picture/{item_id}",
                "url": f"https://automationexercise.com/product_details/{item_id}",
            })

        return jsonify({"status": "success", "count": len(results), "products": results})

    except Exception as err:
        logger.error(f"Search API error: {err}")
        return jsonify({"status": "error", "count": 0, "products": []}), 500


if __name__ == "__main__":
    print("\nStarting dashboard at http://127.0.0.1:5000")
    app.run(debug=True, host="127.0.0.1", port=5000)