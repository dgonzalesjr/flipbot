import os
import json
import base64
import gspread
from oauth2client.service_account import ServiceAccountCredentials


def get_buyers_from_sheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

    creds_raw = os.getenv("GOOGLE_SHEETS_CREDENTIALS_JSON")
    if creds_raw:
        creds_dict = json.loads(base64.b64decode(creds_raw).decode())
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    else:
        creds = ServiceAccountCredentials.from_json_keyfile_name("google_creds.json", scope)

    client = gspread.authorize(creds)
    sheet = client.open("Buyer Leads").sheet1
    data = sheet.get_all_records()

    # Transform into FlipBot-compatible buyer objects
    buyers = []
    for row in data:
        buyer = {
            "name": row.get("Name"),
            "email": row.get("Email"),
            "max_price": float(row.get("Max Price", 0)),
            "wants": [row.get("Card Name")] if row.get("Card Name") else []
        }
        buyers.append(buyer)

    return buyers
