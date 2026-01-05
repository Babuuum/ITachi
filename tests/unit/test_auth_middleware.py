import httpx
import pytest
from fastapi import Depends, FastAPI, Request

from api.dependencies.auth import require_auth
from api.middlewares.auth import AuthMiddleware

pytestmark = pytest.mark.anyio


def create_app(token: str) -> tuple[FastAPI, str]:
    app = FastAPI()
    app.add_middleware(AuthMiddleware, token=token, exempt_paths={"/public"})

    @app.get("/public")
    async def public_endpoint():
        return {"status": "ok"}

    @app.get("/protected")
    async def protected_endpoint(request: Request):
        # request.state.is_auth is set by middleware
        return {"is_auth": getattr(request.state, "is_auth", False)}

    @app.get("/protected-with-dep", dependencies=[Depends(require_auth)])
    async def protected_with_dep():
        return {"status": "ok"}

    return app, token


async def make_client():
    token = "secret-token"
    app, token = create_app(token)
    transport = httpx.ASGITransport(app=app)
    client = httpx.AsyncClient(transport=transport, base_url="http://test")
    return client, token


async def test_exempt_path_allows_without_auth():
    client, _ = await make_client()
    async with client:
        response = await client.get("/public")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


async def test_missing_header_returns_unauthorized():
    client, _ = await make_client()
    async with client:
        response = await client.get("/protected")
    assert response.status_code == 401
    assert response.json() == {"detail": "Missing Authorization header"}


async def test_invalid_token_returns_forbidden():
    client, _ = await make_client()
    async with client:
        response = await client.get("/protected", headers={"Authorization": "Bearer wrong"})
    assert response.status_code == 403
    assert response.json() == {"detail": "Invalid token"}


async def test_valid_token_sets_state_and_passes():
    client, token = await make_client()
    async with client:
        response = await client.get("/protected", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json() == {"is_auth": True}


async def test_dependency_blocks_without_auth():
    client, _ = await make_client()
    async with client:
        response = await client.get("/protected-with-dep")
    assert response.status_code == 401
    assert response.json() == {"detail": "Missing Authorization header"}


async def test_dependency_allows_with_auth():
    client, token = await make_client()
    async with client:
        response = await client.get("/protected-with-dep", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
