import json
from logger import log_match
from notifier import send_discord_alert
from stripe_checkout import create_checkout_session

# Simulated buyer demand (could eventually come from Reddit or DB)
buyers = [
    {"card_name": "Charizard", "max_price": 400},
    {"card_name": "Shining Magikarp", "max_price": 200},
    {"card_name": "Blaine's Arcanine", "max_price": 100}
]


def match_listing(parsed_output, buyers):
    try:
        parsed = json.loads(parsed_output)  # convert string to dict
    except json.JSONDecodeError:
        return "❌ Error parsing AI output."

    for buyer in buyers:
        if buyer["card_name"].lower() in parsed["card_name"].lower():
            if parsed["price"] <= buyer["max_price"]:

                # ✅ Log to CSV
                log_match(
                    card_name=parsed["card_name"],
                    price=parsed["price"],
                    buyer_max=buyer["max_price"],
                    url=parsed.get("url", "https://example.com")
                )

                # ✅ Create Stripe Checkout link
                checkout_url = create_checkout_session(
                    card_name=parsed["card_name"],
                    price=parsed["price"],
                    url=parsed.get("url", "https://example.com")
                )

                # ✅ Send Discord Alert (with Stripe link)
                send_discord_alert(
                    card_name=parsed["card_name"],
                    price=parsed["price"],
                    buyer_max=buyer["max_price"],
                    url=parsed.get("url", "https://example.com"),
                    checkout_url=checkout_url
                )

                return f"🎯 MATCH: {parsed['card_name']} at ${parsed['price']} (buyer max: ${buyer['max_price']})"

    return "❌ No match"
