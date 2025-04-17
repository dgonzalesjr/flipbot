import requests

WEBHOOK_URL = "https://discord.com/api/webhooks/1361947864263163914/XHpr14H2CjNC835ItSQcdUzxvBnXyplMP_MCHljEbVj-XD6-tx-ChC4W4a23IbS7AjTy"

payload = {
    "embeds": [{
        "title": "🎯 MATCH FOUND: Charizard",
        "description": "**Price**: $350\n**Buyer Max**: $400\n[View Listing](https://example.com)",
        "color": 0x00ff00,
        "footer": {"text": "FlipBot Auto Arbitrage"}
    }],
    "components": [
        {
            "type": 1,
            "components": [
                {
                    "type": 2,
                    "label": "💳 Buy Now",
                    "style": 5,
                    "url": "https://example.com/checkout"
                }
            ]
        }
    ]
}

res = requests.post(WEBHOOK_URL, json=payload)
print("✅ Sent!" if res.status_code == 204 else res.text)
