"""
Home Endpoint
"""
from fastapi import APIRouter
from starlette.responses import HTMLResponse

router = APIRouter()

@router.get("/", response_class=HTMLResponse, tags=["Home"], include_in_schema=False)
def home():
    """
    Welcome endpoint.
    Returns an HTML welcome message.
    """
    html_content = """
    <!DOCTYPE html>
    <html>
        <head>
            <title>Welcome to Albz</title>
        </head>
        <body style="text-align: center;">
            <h1>Welcome to Notez BE!</h1>
            <p>This is the main <code>/api/v1</code> entry point for the Notes Be API.</p>
            <p>Visit <a href="/docs">API Documentation</a> for more info.</p>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)
