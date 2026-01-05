from fastapi import HTTPException, Request, status


async def require_auth(request: Request):
    if not getattr(request.state, "is_auth", False):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )
