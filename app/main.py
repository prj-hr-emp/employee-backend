from fastapi import FastAPI
from app.api.routes import router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="HR Pulse - Gamified HR Management")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
