from fastapi import FastAPI
from app.api.v1.endpoints import note

app = FastAPI()

app.include_router(note.router, prefix="/api/v1/notes")
