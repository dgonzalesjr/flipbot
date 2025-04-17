import os
import requests
from dotenv import load_dotenv
import base64

load_dotenv()

EBAY_CLIENT_ID = os.getenv("EBAY_CLIENT_ID")
EBAY_CLIENT_SECRET = os.getenv("EBAY_CLIENT_SECRET")

TOKEN_URL = "https://api.ebay.com/identity/v1/oauth2/token"
SEARCH_URL = "https://api.ebay.com/buy/browse/v1/item_summary/search"


# Get OAuth2 token
def get_ebay_token():
    client_id = os.getenv("EBAY_CLIENT_ID")
    client_secret = os.getenv("EBAY_CLIENT_SECRET")

    if not client_id or not client_secret:
        raise ValueError("❌ Missing eBay client ID or secret.")

    # 🔐 Encode credentials for Basic Auth
    credentials = f"{client_id}:{client_secret}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {encoded_credentials}"
    }

    data = {
        "grant_type": "client_credentials",
        "scope": "https://api.ebay.com/oauth/api_scope"
    }

    print("📡 Requesting token from eBay...")
    response = requests.post(
        "https://api.ebay.com/identity/v1/oauth2/token",
        headers=headers,
        data=data
    )

    if response.status_code != 200:
        print("❌ Error status code:", response.status_code)
        print("❌ Error body:", response.text)
        response.raise_for_status()

    access_token = response.json()["access_token"]
    print("✅ Got access token!")
    return access_token


# Encode client_id:client_secret to base64
def get_basic_auth_token():
    creds = f"{EBAY_CLIENT_ID}:{EBAY_CLIENT_SECRET}"
    return base64.b64encode(creds.encode()).decode()


# Call Browse API search endpoint
def search_ebay_items(query="pokemon charizard", limit=5):
    token = get_ebay_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    params = {
        "q": query,
        "limit": limit
    }
    response = requests.get(SEARCH_URL, headers=headers, params=params)
    response.raise_for_status()
    return response.json()["itemSummaries"]


if __name__ == "__main__":
    results = search_ebay_items()
    for item in results:
        title = item.get("title")
        price = item.get("price", {}).get("value")
        currency = item.get("price", {}).get("currency")
        url = item.get("itemWebUrl")
        print(f"{title} - {price} {currency} - {url}")
