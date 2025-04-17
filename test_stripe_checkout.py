from stripe_checkout import create_checkout_session

checkout_link = create_checkout_session(
    card_name="Shining Magikarp",
    price=180,
    url="https://example.com/test-listing"
)

print("🔗 Stripe Checkout URL:", checkout_link)
