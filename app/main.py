"""
Main: Entry point for execution
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.v1.endpoints import login, note, user, home
from app.core.rate_limit_middleware import RateLimitMiddleware

app = FastAPI(
    title="Notes BE",
    description="An API for creating and managing notes",
    version="1.0.0",
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
)

origins = ["http://localhost:5173",
           "https://albertobarrago.github.io", ]

app.add_middleware(
    RateLimitMiddleware
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["Authorization", "Content-Type"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(home.router, tags=["home"])
app.include_router(login.router, prefix="/api/v1", tags=["Login"])
app.include_router(user.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(note.router, prefix="/api/v1/notes", tags=["Notes"])
