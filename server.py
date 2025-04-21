from fastapi import FastAPI, Request
import uvicorn
import logging
from matchmaker import run_flipbot

app = FastAPI()


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
    print("📬 Form data received:", data)  # <- Required for confirmation in logs


if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000)
