# send_email.py
import os
import requests

MAILGUN_API_KEY = os.getenv("MAILGUN_API_KEY")
MAILGUN_DOMAIN = os.getenv("MAILGUN_DOMAIN")
SENDER_EMAIL = os.getenv("SENDER_EMAIL", f"FlipBot <mailgun@{MAILGUN_DOMAIN}>")


def send_confirmation_email(name, email, card_name):
    subject = "🧾 FlipBot Order Confirmation"
    body = f"""
    Hi {name},

    Thanks for your FlipBot purchase request! We've logged your interest in:

    🔹 {card_name}

    Our team is now processing your order and will be in touch if anything is needed.

    — FlipBot 🤖
    """

    try:
        response = requests.post(
            f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages",
            auth=("api", MAILGUN_API_KEY),
            data={
                "from": SENDER_EMAIL,
                "to": [email],
                "subject": subject,
                "text": body
            }
        )
        response.raise_for_status()
        print("✅ Confirmation email sent.")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
