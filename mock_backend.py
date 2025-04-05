# mock_backend.py
from fastapi import FastAPI, Request

app = FastAPI()

@app.post("/api/request")
async def handle_request(request: Request):
    data = await request.json()
    print("🛎️ Received request from frontend:", data)
    return {"status": "ok"}