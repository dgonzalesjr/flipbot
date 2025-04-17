import csv
import os
from datetime import datetime
import subprocess
import platform

LOG_FILE = "flip_log.csv"


def log_match(card_name, price, buyer_max, url):
    file_exists = os.path.isfile(LOG_FILE)

    try:
        margin = float(buyer_max) - float(price)
    except (ValueError, TypeError):
        margin = "N/A"

    with open(LOG_FILE, mode="a", newline="") as file:
        writer = csv.writer(file)
        if not file_exists:
            # Write header if file is new
            writer.writerow(
                [
                    "Timestamp",
                    "Card Name",
                    "Price",
                    "Buyer Max",
                    "URL",
                    "Margin"
                ]
            )
        writer.writerow(
            [
                datetime.now(),
                card_name,
                price,
                buyer_max,
                url,
                margin
            ]
        )


def open_csv():
    if platform.system() == "Darwin":  # macOS
        subprocess.call(["open", LOG_FILE])
    elif platform.system() == "Windows":
        subprocess.call(["start", LOG_FILE], shell=True)
    elif platform.system() == "Linux":
        subprocess.call(["xdg-open", LOG_FILE])
    else:
        print("⚠️ Auto-open not supported on this OS.")
