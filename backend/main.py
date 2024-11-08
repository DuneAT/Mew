from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api import ask_routes, file_routes

app = FastAPI()

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(ask_routes.router)
app.include_router(file_routes.router)
