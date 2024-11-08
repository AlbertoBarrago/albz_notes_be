"""
Main: Entry point for execution
"""
from fastapi import FastAPI

from app.api.v1.endpoints import auth, note, home

app = FastAPI(
    title="Notes BE",
    description="An API for creating and managing notes",
    version="1.0.0",
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
)


app.include_router(home.router, tags=["home"])
app.include_router(auth.router, prefix="/api/v1", tags=["Auth"])
app.include_router(note.router, prefix="/api/v1/notes", tags=["Notes"])
