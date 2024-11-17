from fastapi import APIRouter, Request
from backend.utils.server_utils import request_answer, request_answer_with_retrieval, request_answer_with_retrieval_legifrance

router = APIRouter()


@router.post("/api/ask")
async def ask(request: Request):
    data = await request.json()
    prompt = data.get("prompt")
    response = request_answer(prompt)
    return {"response": response}


@router.post("/api/ask_rag")
async def ask(request: Request):
    data = await request.json()
    prompt = data.get("prompt")
    response = request_answer_with_retrieval(prompt)
    return {"response": response}


@router.post("/api/ask_legifrance")
async def ask(request: Request):
    data = await request.json()
    prompt = data.get("prompt")
    response = request_answer_with_retrieval_legifrance(prompt)
    return {"response": response}
