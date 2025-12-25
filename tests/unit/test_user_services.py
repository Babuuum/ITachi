from unittest.mock import AsyncMock

import pytest

from core.services.tg_bot import user_services

pytestmark = pytest.mark.anyio


class FakeSession:
    """Minimal async session mock that supports `async with session.begin()`."""

    def __init__(self):
        self.close = AsyncMock()

    def begin(self):
        return self

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return False


async def test_user_auth_success(monkeypatch):
    fake_session = FakeSession()
    monkeypatch.setattr(user_services, "session", fake_session)

    mock_get_or_create = AsyncMock(return_value="user_obj")
    monkeypatch.setattr(
        user_services.UserService,
        "get_or_create_user",
        mock_get_or_create,
    )

    result = await user_services.user_authorization(user_tg_id=1, username="nick")

    mock_get_or_create.assert_awaited_once_with(
        fake_session,
        tg_id=1,
        tg_nickname="nick",
    )
    fake_session.close.assert_awaited_once()
    assert result == "user_obj"


async def test_user_auth_error_closes_session(monkeypatch):
    fake_session = FakeSession()
    monkeypatch.setattr(user_services, "session", fake_session)

    mock_get_or_create = AsyncMock(side_effect=RuntimeError("boom"))
    monkeypatch.setattr(
        user_services.UserService,
        "get_or_create_user",
        mock_get_or_create,
    )

    with pytest.raises(TypeError):
        await user_services.user_authorization(user_tg_id=2, username="err")

    fake_session.close.assert_awaited_once()
