import os
import requests

EBAY_OAUTH_TOKEN = os.getenv("EBAY_OAUTH_TOKEN")


def place_ebay_order(item_id, name, email, address):
    url = "https://api.ebay.com/buy/order/v1/guest_checkout_session/initiate"
    headers = {
        "Authorization": f"Bearer {EBAY_OAUTH_TOKEN}",
        "Content-Type": "application/json"
    }

    body = {
        "contactEmail": email,
        "shippingAddress": {
            "fullName": name,
            "addressLine1": address,
            "city": "CityName",      # ← You'll need to parse or collect these from the form
            "stateOrProvince": "CA",
            "postalCode": "92101",
            "country": "US"
        },
        "lineItemInputs": [
            {
                "itemId": item_id,
                "quantity": 1
            }
        ]
    }

    response = requests.post(url, headers=headers, json=body)
    print("eBay order response:", response.status_code, response.text)
