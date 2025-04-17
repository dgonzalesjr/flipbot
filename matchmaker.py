import json
import schedule
import time
import sys
import random
from search_ebay_browse import search_ebay_items
from logger import log_match
from notifier import send_discord_alert
# from buyer_loader import get_buyers_from_sheet

# Simulated buyer demand (like Reddit WTB posts)
# buyers = get_buyers_from_sheet()

buyers = buyers = [
    {"card_name": "Shining Magikarp", "max_price": 1000},  # Set high on purpose
    {"card_name": "Charizard", "max_price": 1000},
    {"card_name": "Blaine's Arcanine", "max_price": 1000}
]


def match_listing(parsed_output, buyers):
    try:
        parsed = json.loads(parsed_output)
    except json.JSONDecodeError:
        return "❌ Error parsing AI output."

    matched = False

    for buyer in buyers:
        if buyer["card_name"].lower() in parsed["card_name"].lower():
            if parsed["price"] <= buyer["max_price"]:
                send_discord_alert(
                    card_name=parsed["card_name"],
                    price=parsed["price"],
                    buyer_max=buyer["max_price"],
                    url=parsed.get("url", "https://example.com")
                )
                matched = True
                break

    # Log all listings, even if no match
    log_match(
        card_name=parsed["card_name"],
        price=parsed["price"],
        buyer_max=buyer["max_price"] if matched else "N/A",
        url=parsed.get("url", "https://example.com")
    )

    if matched:
        return f"🎯 MATCH: {parsed['card_name']} at ${parsed['price']} (buyer max: ${buyer['max_price']})"
    else:
        return f"⛔ No match: {parsed['card_name']} at ${parsed['price']}"


def match_from_browse_api(queries=None, limit=10):
    if queries is None:
        queries = ["Charizard", "Blastoise", "Lugia", "Shining Magikarp"]

    for query in queries:
        print(f"\n🔍 Searching eBay for: {query}")
        try:
            listings = search_ebay_items(query=query, limit=limit)
        except Exception as e:
            print(f"⚠️ API error for query '{query}': {e}")
            continue

        for item in listings:
            card_name = item.get("title", "")
            price = float(item.get("price", {}).get("value", 0))
            currency = item.get("price", {}).get("currency")
            url = item.get("itemWebUrl")

            parsed = {
                "card_name": card_name,
                "price": price,
                "currency": currency,
                "url": url
            }

            match_message = match_listing(json.dumps(parsed), buyers)
            print(match_message)

        # Rate limit buffer between queries
        delay = random.uniform(1.5, 3.0)
        print(f"⏳ Waiting {delay:.2f} seconds before next query...")
        time.sleep(delay)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "now":
        print("▶️ Running FlipBot once on demand...")
        match_from_browse_api()
    else:
        schedule.every(15).minutes.do(match_from_browse_api)
        print("⏱ FlipBot scheduler started. Running every 15 minutes...")
        while True:
            schedule.run_pending()
            time.sleep(1)


def run_flipbot():
    match_from_browse_api()
