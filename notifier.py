import os
import requests
from dotenv import load_dotenv

load_dotenv()
WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK")


def send_discord_alert(card_name, price, buyer_max, url, checkout_url=None):
    if not WEBHOOK_URL:
        print("🚫 No webhook URL set.")
        return

    message_content = (
        f"🎯 **MATCH FOUND**\n"
        f"**Card**: {card_name}\n"
        f"**Price**: ${price}\n"
        f"**Buyer Max**: ${buyer_max}\n"
        f"🔗 [View Listing]({url})"
    )

    if checkout_url:
        message_content += f"\n💳 [Buy Now]({checkout_url})"

    message = {
        "embeds": [{
            "title": f"🎯 MATCH FOUND: {card_name}",
            "description": (
                f"**Price**: ${price}\n**Buyer Max**:"
                f"${buyer_max}\n[View Listing]({url})"
            ),
            "color": 0x00ff00,  # green highlight
            "footer": {"text": "FlipBot Auto Arbitrage"},
            # Optional thumbnail
            # "thumbnail": {"url": "https://your-image-link.com/card.jpg"}
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
