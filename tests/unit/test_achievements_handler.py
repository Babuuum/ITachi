import types
from unittest.mock import AsyncMock, call

import pytest

from bot.handlers.achievements import achievements


pytestmark = pytest.mark.anyio


class DummyUser:
    def __init__(self, is_active: bool = True):
        self.is_active = is_active


def build_message(tg_id: int, username: str | None) -> object:
    from_user = types.SimpleNamespace(id=tg_id, username=username)
    return types.SimpleNamespace(from_user=from_user, answer=AsyncMock())


async def test_achievements_success(monkeypatch):
    message = build_message(tg_id=1, username="tester")

    mock_auth = AsyncMock(return_value=DummyUser())
    monkeypatch.setattr("bot.handlers.achievements.user_auth", mock_auth)

    ach_list = [
        types.SimpleNamespace(name="test_1", description="desc1"),
        types.SimpleNamespace(name="test_2", description="desc2"),
    ]
    mock_get = AsyncMock(return_value=ach_list)
    monkeypatch.setattr("bot.handlers.achievements.get_achievements", mock_get)

    fake_session = object()
    await achievements(message, session=fake_session)

    mock_auth.assert_awaited_once_with(session=fake_session, message=message)
    mock_get.assert_awaited_once_with(session=fake_session)
    message.answer.assert_awaited_once_with("Все достижения:\n- test_1: desc1\n- test_2: desc2")


async def test_achievements_user_not_found(monkeypatch):
    message = build_message(tg_id=2, username="missing")

    mock_auth = AsyncMock(return_value=DummyUser())
    monkeypatch.setattr("bot.handlers.achievements.user_auth", mock_auth)

    mock_get = AsyncMock()
    monkeypatch.setattr("bot.handlers.achievements.get_achievements", mock_get)

    fake_session = object()
    await achievements(message, session=fake_session)

    mock_auth.assert_awaited_once_with(session=fake_session, message=message)
    mock_get.assert_awaited_once_with(session=fake_session)


async def test_achievements_empty_list(monkeypatch):
    message = build_message(tg_id=3, username="empty")

    mock_auth = AsyncMock(return_value=DummyUser())
    monkeypatch.setattr("bot.handlers.achievements.user_auth", mock_auth)

    mock_get = AsyncMock(return_value=[])
    monkeypatch.setattr("bot.handlers.achievements.get_achievements", mock_get)

    fake_session = object()
    await achievements(message, session=fake_session)

    mock_auth.assert_awaited_once_with(session=fake_session, message=message)
    mock_get.assert_awaited_once_with(session=fake_session)
    assert message.answer.await_args_list == [call("У вас нет доступных достижений.")]
