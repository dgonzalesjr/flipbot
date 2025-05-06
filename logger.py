import csv
import os
from datetime import datetime
import subprocess
import platform
import json
import base64
import gspread
from oauth2client.service_account import ServiceAccountCredentials

LOG_FILE = "flip_log.csv"
SHEET_NAME = "FlipBot Log"
SHEET_TAB = "log"


def get_google_sheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

    creds_raw = os.getenv("GOOGLE_SHEETS_CREDENTIALS_JSON")
    if creds_raw:
        creds_dict = json.loads(base64.b64decode(creds_raw).decode())
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    else:
        creds = ServiceAccountCredentials.from_json_keyfile_name("google_creds.json", scope)

    client = gspread.authorize(creds)
    sheet = client.open(SHEET_NAME).worksheet(SHEET_TAB)
    return sheet


def log_match(card_name, price, buyer_max, url):
    try:
        margin = float(buyer_max) - float(price)
    except (ValueError, TypeError):
        margin = "N/A"

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    row = [timestamp, card_name, price, buyer_max, url, margin]

    # Log to Google Sheets
    try:
        sheet = get_google_sheet()
        sheet.append_row(row)
        print("✅ Logged to Google Sheets.")
    except Exception as e:
        print(f"⚠️ Google Sheets logging failed: {e}")

    # Also log to local CSV as fallback
    file_exists = os.path.isfile(LOG_FILE)
    with open(LOG_FILE, mode="a", newline="") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Timestamp", "Card Name", "Price", "Buyer Max", "URL", "Margin"])
        writer.writerow(row)


def log_evaluation(evaluation: dict):
    try:
        sheet = get_google_sheet(sheet_name="FlipBot Evaluator Log", tab_name="evaluator_log")
        sheet.append_row([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            evaluation["title"],
            evaluation["price"],
            evaluation["resale_value"],
            evaluation["condition"],
            evaluation["grade"],
            evaluation["profit_estimate"],
            evaluation["should_buy"],
            evaluation["reason"]
        ])
        print("🧠 Logged evaluation to separate Google Sheet.")
    except Exception as e:
        print(f"⚠️ Evaluation Google Sheets logging failed: {e}")

    # Local fallback
    file_exists = os.path.isfile("evaluation_log.csv")
    with open("evaluation_log.csv", mode="a", newline="") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow([
                "Timestamp", "Title", "Price", "Resale Value", "Condition", 
                "Grade", "Profit Estimate", "Should Buy", "Reason"
            ])
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            evaluation["title"],
            evaluation["price"],
            evaluation["resale_value"],
            evaluation["condition"],
            evaluation["grade"],
            evaluation["profit_estimate"],
            evaluation["should_buy"],
            evaluation["reason"]
        ])


def open_csv():
    if platform.system() == "Darwin":  # macOS
        subprocess.call(["open", LOG_FILE])
    elif platform.system() == "Windows":
        subprocess.call(["start", LOG_FILE], shell=True)
    elif platform.system() == "Linux":
        subprocess.call(["xdg-open", LOG_FILE])
    else:
        print("⚠️ Auto-open not supported on this OS.")
