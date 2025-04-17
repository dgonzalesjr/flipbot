import requests

WEBHOOK_URL = "https://discord.com/api/webhooks/1361856276740702318/iRBBHAn1p-qRBUp9wor7SQ2h32qtisAAhlYG-KdFQUCGLg6SegXsVNrZgkMoP6Ly0lkx"

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
