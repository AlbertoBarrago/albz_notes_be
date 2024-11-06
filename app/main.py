from fastapi import FastAPI
from app.api.v1.endpoints import notes

app = FastAPI()

app.include_router(notes.router, prefix="/api/v1/notes")
