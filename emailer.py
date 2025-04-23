import os
import requests

MAILGUN_API_KEY = os.getenv("MAILGUN_API_KEY")
MAILGUN_DOMAIN = os.getenv("MAILGUN_DOMAIN")
FROM_EMAIL = f"FlipBot Orders <mailgun@{MAILGUN_DOMAIN}>"


def send_confirmation_email(name, email, address, product_name, price, product_type="item"):
    html = f"""
    <!DOCTYPE html>
    <html>
      <head>
        <meta charset="UTF-8" />
        <style>
          body {{
            font-family: 'Helvetica Neue', sans-serif;
            background-color: #f9fafb;
            padding: 20px;
            color: #333;
          }}
          .container {{
            max-width: 600px;
            margin: auto;
            background: #ffffff;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.05);
          }}
          h2 {{
            color: #1d4ed8;
          }}
          .summary {{
            margin-top: 20px;
            padding: 15px;
            background: #eff6ff;
            border-left: 4px solid #3b82f6;
          }}
          .footer {{
            font-size: 0.85em;
            color: #888;
            margin-top: 30px;
            text-align: center;
          }}
        </style>
      </head>
      <body>
        <div class="container">
          <h2>🎉 Order Received, {name}!</h2>
          <p>Thanks for your interest in this {product_type}.
          We're now processing your order and will notify you once it's on the way.</p>

          <div class="summary">
            <strong>Product:</strong> {product_name}<br/>
            <strong>Price:</strong> ${price}<br/>
            <strong>Shipping To:</strong><br/>
            {address}
          </div>

          <p>If you have any questions, feel free to reply to this email.</p>

          <div class="footer">
            We appreciate your trust — and can't wait to flip more great deals for you.
          </div>
        </div>
      </body>
    </html>
    """

    return requests.post(
        f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages",
        auth=("api", MAILGUN_API_KEY),
        data={
            "from": FROM_EMAIL,
            "to": email,
            "subject": f"Your FlipBot Order for {product_name} is Confirmed!",
            "html": html
        }
    )
