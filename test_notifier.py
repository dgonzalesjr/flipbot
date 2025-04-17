from notifier import send_discord_alert

# Test sample card
send_discord_alert(
    card_name="Shining Magikarp",
    price=180,
    buyer_max=200,
    url="https://example.com/test-listing"
)
