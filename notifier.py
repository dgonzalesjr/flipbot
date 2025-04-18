import os
import requests
from dotenv import load_dotenv

load_dotenv()
WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK")


def get_card_image_url(card_name):
    card_name = card_name.lower()
    if "charizard" in card_name:
        return "https://images.pokemontcg.io/base1/4_hires.png"
    if "magikarp" in card_name:
        return "https://images.pokemontcg.io/neo3/66_hires.png"
    if "arcanine" in card_name:
        return "https://images.pokemontcg.io/gym2/6_hires.png"
    return "https://images.pokemontcg.io/base1/1_hires.png"  # fallback


def send_discord_alert(card_name, price, buyer_max, url, checkout_url=None):
    if not WEBHOOK_URL:
        print("🚫 No webhook URL set.")
        return

    image_url = get_card_image_url(card_name)

    message = {
        "embeds": [{
            "title": f"🎯 MATCH FOUND: {card_name}",
            "description": (
                f"**Price**: ${price}\n"
                f"**Buyer Max**: ${buyer_max}\n"
                f"[View Listing]({url})"
            ),
            "color": 0x00ff00,  # green
            "image": {"url": image_url},
            "footer": {"text": "FlipBot Auto Arbitrage"}
        }],
        "components": [
            {
                "type": 1,  # Action row
                "components": [
                    {
                        "type": 2,  # Button
                        "label": "💳 Buy Now",
                        "style": 5,  # Link button
                        "url": checkout_url if checkout_url else url
                    }
                ]
            }
        ]
    }

    response = requests.post(WEBHOOK_URL, json=message)

    if response.status_code == 204:
        print("✅ Discord alert sent!")
    else:
        print(f"⚠️ Discord error: {response.status_code} - {response.text}")
