import os
import requests
from dotenv import load_dotenv

load_dotenv()
app_id = os.getenv("EBAY_APP_ID")


def search_ebay_pokemon_cards(keywords="pokemon", max_price=200, limit=5):
    url = "https://svcs.ebay.com/services/search/FindingService/v1"

    params = {
        "OPERATION-NAME": "findItemsByKeywords",
        "SERVICE-VERSION": "1.0.0",
        "SECURITY-APPNAME": app_id,
        "RESPONSE-DATA-FORMAT": "JSON",
        "REST-PAYLOAD": "",
        "keywords": keywords,
        "paginationInput.entriesPerPage": limit,
        "itemFilter(0).name": "MaxPrice",
        "itemFilter(0).value": str(max_price),
        "itemFilter(1).name": "Currency",
        "itemFilter(1).value": "USD"
    }

    print("⏳ Sending request to eBay...")
    response = requests.get(url, params=params)
    print("📡 Status:", response.status_code)

    try:
        data = response.json()
    except Exception as e:
        print("❌ JSON parse failed:", e)
        return []

    if response.status_code != 200:
        print("❌ Error response:")
        print(data.get("errorMessage", data))
        return []

    items = data.get("findItemsByKeywordsResponse", [])[0].get("searchResult", [])[0].get("item", [])

    results = []
    for item in items:
        title = item.get("title", [""])[0]
        price = item.get(
            "sellingStatus", [{}])[0].get("currentPrice", [{}])[0].get("__value__", "0")
        url = item.get("viewItemURL", [""])[0]
        results.append({
            "title": title,
            "price": float(price),
            "url": url
        })

    return results


if __name__ == "__main__":
    listings = search_ebay_pokemon_cards()
    if not listings:
        print("🚫 No listings found.")
    else:
        for l in listings:
            print(f"🎴 {l['title']} - ${l['price']} - {l['url']}")
