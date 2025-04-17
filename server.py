from fastapi import FastAPI
import uvicorn
from matchmaker import run_flipbot

app = FastAPI()


@app.get("/")
def home():
    return {"message": "FlipBot is alive!"}


@app.post("/trigger")
def trigger():
    run_flipbot()
    return {"status": "FlipBot triggered!"}


if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000)
