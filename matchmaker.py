import json
import schedule
import time
import sys
import random
from search_ebay_browse import search_ebay_items
from logger import log_match
from logger import log_evaluation  # New
from notifier import send_discord_alert
from utils.margin_calc import calculate_margin
from card_evaluator import evaluate_card

# Simulated buyer demand
buyers = [
    {"card_name": "Shining Magikarp", "max_price": 1000},
    {"card_name": "Charizard", "max_price": 1000},
    {"card_name": "Blaine's Arcanine", "max_price": 1000}
]

# 🔘 Toggle test injection
INJECT_TEST_CARD = True


def match_listing(parsed_output, buyers):
    try:
        parsed = json.loads(parsed_output)
    except json.JSONDecodeError:
        return "❌ Error parsing AI output."

    matched = False

    for buyer in buyers:
        if buyer["card_name"].lower() in parsed["card_name"].lower():
            if parsed["price"] <= buyer["max_price"]:

                # 🧠 AI Evaluator: Check listing quality/value
                evaluation = evaluate_card(parsed["card_name"], parsed["price"])
                log_evaluation(evaluation, parsed.get("url", "N/A"))

                if not evaluation["should_buy"]:
                    print(f"🤖 Skipping {parsed['card_name']} — not profitable: {evaluation['reason']}")
                    return f"⚠️ AI skipped: {parsed['card_name']} — {evaluation['reason']}"

                # 📊 Margin check
                result = calculate_margin(
                    ebay_price=parsed["price"],
                    stripe_sale_price=buyer["max_price"]
                )

                if not result["should_buy"]:
                    print(
                        f"❌ Skipping {parsed['card_name']} — margin too low:"
                        f" ${result['net_profit']} ({result['margin_percent']}%)"
                    )
                    return f"⚠️ Margin too low: {parsed['card_name']}"

                # ✅ Proceed with alert
                send_discord_alert(
                    card_name=parsed["card_name"],
                    price=parsed["price"],
                    buyer_max=buyer["max_price"],
                    url=parsed.get("url", "https://example.com")
                )
                matched = True
                break

    # Log all listings regardless of match
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

    # 🧪 Inject test card directly
    if INJECT_TEST_CARD:
        test_card = {
            "card_name": "Charizard GX Mint Condition",
            "price": 10.00,
            "currency": "USD",
            "url": "https://example.com/charizard"
        }
        print("\n🧪 Injecting test card for evaluation...")
        match_message = match_listing(json.dumps(test_card), buyers)
        print(match_message)

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

        delay = random.uniform(1.5, 3.0)
        print(f"⏳ Waiting {delay:.2f} seconds before next query...")
        time.sleep(delay)


def run_flipbot():
    match_from_browse_api()


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
