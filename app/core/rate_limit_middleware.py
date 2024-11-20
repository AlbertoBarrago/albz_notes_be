"""
 Rate limit middleware
"""
from datetime import datetime, timedelta
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from app.core.access_token import decode_access_token
from app.core.settings import settings
from app.db.models.rate_limit import RateLimit
from app.db.mysql import SessionLocal


def _get_identifier(request: Request, ip: str) -> str:
    """Extract identifier from request"""
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.startswith('Bearer '):
        try:
            username = decode_access_token(auth_header.split(' ')[1])
            return f"user:{username}"
        except HTTPException:
            return f"ip:{ip}"
    return f"ip:{ip}"


def _get_or_create_rate_limit(identifier: str,
                              now: datetime,
                              window_start: datetime,
                              db) -> RateLimit:
    """Get or create rate limit record"""
    rate_limit = db.query(RateLimit).filter(
        RateLimit.identifier == identifier,
        RateLimit.timestamp > window_start
    ).first()

    if not rate_limit:
        rate_limit = RateLimit(
            identifier=identifier,
            requests=1,
            timestamp=now
        )
        db.add(rate_limit)
    else:
        rate_limit.requests += 1
        rate_limit.timestamp = now

    return rate_limit


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Rate Limit Middleware"""

    def __init__(self, app):
        super().__init__(app)
        self.rate_limit = int(settings.RATE_LIMIT)
        self.window = int(settings.RATE_LIMIT_WINDOW)

    async def dispatch(self, request: Request, call_next):
        db = SessionLocal()
        try:
            ip = request.client.host
            identifier = _get_identifier(request, ip)

            now = datetime.now()
            window_start = now - timedelta(minutes=self.window)

            rate_limit = _get_or_create_rate_limit(identifier, now, window_start, db)

            if rate_limit.requests > self.rate_limit:
                return JSONResponse(
                    status_code=429,
                    content={"detail": "Rate limit exceeded"}
                )

            db.commit()
            return await call_next(request)
        finally:
            db.close()
