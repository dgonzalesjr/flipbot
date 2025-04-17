import os
import stripe
from dotenv import load_dotenv

load_dotenv()
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")


def create_checkout_session(card_name, price, url):
    try:
        session = stripe.checkout.Session.create(
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': f"Pokémon Flip: {card_name}",
                        'description': f"Direct flip deal from {url}",
                    },
                    'unit_amount': int(float(price) * 100),  # Cents for stripe
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url='https://example.com/success',
            cancel_url='https://example.com/cancel',
        )
        return session.url
    except Exception as e:
        print(f"❌ Stripe error: {e}")
        return None
