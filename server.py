from fastapi import FastAPI, Request
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

from matchmaker import run_flipbot

app = FastAPI()
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
    print("📬 Form data received:", data)  # <- Required for confirmation in logs


if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000)
