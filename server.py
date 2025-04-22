from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import logging
from matchmaker import run_flipbot
from ebay_order import place_ebay_order
from db import init_db, log_submission
from notifier import send_discord_alert

app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize SQLite database
init_db()

# Allow GitHub Pages access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://dgonzalesjr.github.io"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "FlipBot is alive!"}


@app.post("/trigger")
def trigger():
    run_flipbot()
    return {"status": "FlipBot triggered!"}


@app.post("/api/form-submitted")
async def form_submitted(request: Request):
    data = await request.json()
    logging.info("📬 Received form submission.")

    item_id = data.get("ebay_item_id")
    address = data.get("address")
    name = data.get("name")
    email = data.get("email")
    card_name = data.get("card_name", "Unknown")

    # Log to SQLite
    try:
        log_submission(name, email, address, card_name, item_id)
        logging.info("🗃 Submission logged in SQLite.")
    except Exception as e:
        logging.error(f"❌ Failed to log submission: {e}")

    # Mask email for Discord
    buyer_mask = email.split("@")[0][:3] + "***" if email else "unknown"

    # Attempt eBay order
    if item_id and address:
        logging.info(f"🚀 Attempting mock order for {card_name}")
        place_ebay_order(item_id, name, email, address)
    else:
        logging.warning("⚠️ Missing item_id or address. Order not placed.")

    # Discord notification
    send_discord_alert(
        card_name=card_name,
        price="Submitted",
        buyer_max=buyer_mask,
        url="Shipping form completed ✅"
    )

    return {"status": "received"}

if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000)
