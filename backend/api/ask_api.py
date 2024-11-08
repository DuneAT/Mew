from fastapi import APIRouter
from backend.controllers.ask_controllers import handle_ask_request

router = APIRouter()

router.post("/ask")(handle_ask_request)
