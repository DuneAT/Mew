from fastapi import Request, HTTPException
from backend.services.ask_services import request_answer


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
