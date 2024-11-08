from fastapi import APIRouter, Request
from backend.utils.server_utils import request_answer

router = APIRouter()


@router.post("/api/ask")
async def ask(request: Request):
    data = await request.json()
    prompt = data.get("prompt")
    response = request_answer(prompt)
    return {"response": response}
