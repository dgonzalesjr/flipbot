from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import logging
from matchmaker import run_flipbot
from ebay_order import place_ebay_order
from notifier import send_discord_alert  # Optional: for confirmation pings

app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO)

# Allow GitHub Pages form to access this API
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
    logging.info(f"📬 Form data received: {data}")

    item_id = data.get("ebay_item_id")
    address = data.get("address")
    name = data.get("name")
    email = data.get("email")
    card_name = data.get("card_name", "Unknown")

    if item_id and address:
        logging.info(f"🚀 Attempting to place eBay order for {card_name}")
        place_ebay_order(item_id, name, email, address)
    else:
        logging.warning("⚠️ Missing item_id or address. Order not placed.")

    # Optional: Notify you in Discord
    send_discord_alert(
        card_name=card_name,
        price="Submitted",
        buyer_max=email,
        url="Shipping form completed ✅"
    )

    return {"status": "received"}

if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000)
