from fastapi import Request, HTTPException
from backend.utils.server_utils import request_answer, request_answer_with_retrieval


async def handle_ask_request(request: Request):
    try:
        data = await request.json()
        prompt = data.get("prompt")

        if not prompt:
            raise HTTPException(status_code=400, detail="Prompt is required.")

        response = request_answer(prompt)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def ask(request: Request):
    data = await request.json()
    prompt = data.get("prompt")
    response = request_answer(prompt)
    return {"response": response}


async def ask_rag(request: Request):
    data = await request.json()
    prompt = data.get("prompt")
    response = request_answer_with_retrieval(prompt)
    return {"response": response}
