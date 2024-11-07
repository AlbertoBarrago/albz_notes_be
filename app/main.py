from fastapi import FastAPI
from app.api.v1.endpoints import note, auth

app = FastAPI()


app.include_router(auth.router, prefix="/api/v1", tags=["auth"])
app.include_router(note.router, prefix="/api/v1/notes", tags=["notes"])
