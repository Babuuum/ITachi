from __future__ import annotations

from typing import Iterable

from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware


class AuthMiddleware(BaseHTTPMiddleware):
    """Simple bearer-token middleware for API endpoints."""

    def __init__(self, app, *, token: str, exempt_paths: Iterable[str] | None = None):
        super().__init__(app)
        self.token = token
        self.exempt_paths = set(exempt_paths or ())

    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        if (
            path in self.exempt_paths
            or path.startswith("/docs")
            or path.startswith("/openapi")
            or path.startswith("/redoc")
        ):
            return await call_next(request)

        header = request.headers.get("Authorization")
        if not header or not header.startswith("Bearer "):
            return JSONResponse(
                {"detail": "Missing Authorization header"},
                status_code=status.HTTP_401_UNAUTHORIZED,
            )

        incoming_token = header.removeprefix("Bearer ").strip()
        if incoming_token != self.token:
            return JSONResponse({"detail": "Invalid token"}, status_code=status.HTTP_403_FORBIDDEN)

        request.state.is_auth = True
        return await call_next(request)
