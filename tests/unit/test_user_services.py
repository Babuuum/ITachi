from unittest.mock import AsyncMock

import pytest

from core.utils import user_auth as user_auth_module

pytestmark = pytest.mark.anyio


class FakeSession:
    """Minimal async session mock compatible with async context manager."""

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return False


def make_fake_message(tg_id: int, username: str):
    return type("Msg", (), {"from_user": type("FU", (), {"id": tg_id, "username": username})()})()


async def test_user_auth_success(monkeypatch):
    fake_session = FakeSession()
    fake_message = make_fake_message(1, "nick")

    mock_get_or_create = AsyncMock(return_value="user_obj")
    monkeypatch.setattr(user_auth_module.UserTgService, "get_or_create_user", mock_get_or_create)

    result = await user_auth_module.user_auth(session=fake_session, message=fake_message)

    mock_get_or_create.assert_awaited_once_with(
        fake_session,
        tg_id=1,
        tg_nickname="nick",
    )
    assert result == "user_obj"


async def test_user_auth_error(monkeypatch):
    fake_session = FakeSession()
    fake_message = make_fake_message(2, "err")

    mock_get_or_create = AsyncMock(side_effect=RuntimeError("boom"))
    monkeypatch.setattr(user_auth_module.UserTgService, "get_or_create_user", mock_get_or_create)

    with pytest.raises(RuntimeError):
        await user_auth_module.user_auth(session=fake_session, message=fake_message)


async def test_user_auth_allows_missing_username(monkeypatch):
    fake_session = FakeSession()
    fake_message = make_fake_message(3, None)

    mock_get_or_create = AsyncMock(return_value="user_obj_none")
    monkeypatch.setattr(user_auth_module.UserTgService, "get_or_create_user", mock_get_or_create)

    result = await user_auth_module.user_auth(session=fake_session, message=fake_message)

    mock_get_or_create.assert_awaited_once_with(
        fake_session,
        tg_id=3,
        tg_nickname=None,
    )
    assert result == "user_obj_none"
