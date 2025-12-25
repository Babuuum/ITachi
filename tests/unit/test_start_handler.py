import types
from unittest.mock import AsyncMock

import pytest

from bot.handlers.start import cmd_start

pytestmark = pytest.mark.anyio


class DummyUser:
    def __init__(self, is_active: bool):
        self.is_active = is_active


def build_message(tg_id: int, username: str | None) -> object:
    from_user = types.SimpleNamespace(id=tg_id, username=username)
    message = types.SimpleNamespace(
        from_user=from_user,
        answer=AsyncMock()
    )
    return message


async def test_cmd_start_active_user(monkeypatch):
    fake_user = DummyUser(is_active=True)
    mock_user_auth = AsyncMock(return_value=fake_user)
    monkeypatch.setattr("bot.handlers.start.user_auth", mock_user_auth)

    message = build_message(tg_id=123, username="tester")

    await cmd_start(message)

    mock_user_auth.assert_awaited_once_with(user_tg_id=123, username="tester")
    message.answer.assert_awaited_once_with("Привет, tester!\nСтатус: Активен")


async def test_cmd_start_inactive_user(monkeypatch):
    fake_user = DummyUser(is_active=False)
    mock_user_auth = AsyncMock(return_value=fake_user)
    monkeypatch.setattr("bot.handlers.start.user_auth", mock_user_auth)

    message = build_message(tg_id=456, username="noactive")

    await cmd_start(message)

    mock_user_auth.assert_awaited_once_with(user_tg_id=456, username="noactive")
    message.answer.assert_awaited_once_with("Привет, noactive!\nСтатус: Неактивен")


async def test_cmd_start_without_username(monkeypatch):
    fake_user = DummyUser(is_active=True)
    mock_user_auth = AsyncMock(return_value=fake_user)
    monkeypatch.setattr("bot.handlers.start.user_auth", mock_user_auth)

    message = build_message(tg_id=789, username=None)

    await cmd_start(message)

    mock_user_auth.assert_awaited_once_with(user_tg_id=789, username=None)
    message.answer.assert_awaited_once_with("Привет, None!\nСтатус: Активен")
