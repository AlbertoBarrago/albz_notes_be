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
            <title>Webservice: Notez_Be </title>
            <link rel="icon" type="image/x-icon" href="/static/favicon_io/favicon.ico">
            <link rel="icon" href="data:,">
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <meta name="description" content="Welcome to Notez BE!">
            <meta name="keywords" content="Notez, Albz, API, Documentation">
            <meta name="author" content="Albz">
            <meta name="robots" content="index, follow">
            <meta name="googlebot" content="index, follow">
            <meta name="google" content="notranslate index, follow">
        </head>
        <body style="text-align: center;">
            <h1>Welcome to Notez BE!</h1>
            <p>This is the main <code>/api/v1</code> entry point for the Notes Be API.</p>
            <p>Visit <a href="/docs">API Documentation</a> for more info.</p>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)
