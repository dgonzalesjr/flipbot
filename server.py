from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from matchmaker import run_flipbot
from ebay_order import place_ebay_order

app = FastAPI()

# CORS middleware must come right after FastAPI app declaration
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
    print("Form data received:", data)

    # 🔁 Trigger eBay order placement
    item_id = data.get("ebay_item_id")
    address = data.get("address")
    name = data.get("name")
    email = data.get("email")

    if item_id and address:
        place_ebay_order(item_id, name, email, address)

    return {"status": "received"}

if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000)
