"""
 Main: Entry point for execution
"""
from fastapi.staticfiles import StaticFiles

from app.api.v1.endpoints import (
    login_router,
    notes_router,
    users_router,
    home_router,
    oauth_router
)
from app.core.setup import create_app

app = create_app()
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(home_router, tags=["home"])
app.include_router(
    login_router, prefix="/api/v1", tags=["Login"])
app.include_router(
    oauth_router, prefix="/api/v1", tags=["OAuth"])
app.include_router(
    users_router, prefix="/api/v1/users", tags=["Users"])
app.include_router(
    notes_router, prefix="/api/v1/notes", tags=["Notes"])
