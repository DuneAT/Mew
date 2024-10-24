from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from utils.server_utils import request_answer
import requests
import json

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:11434"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/generate")
async def ask(request: Request):
    data = await request.json()
    prompt = data.get("prompt")
    response = request_answer(prompt)
    return {"response": response}
