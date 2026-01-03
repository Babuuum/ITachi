import pytest
from sqlalchemy import select

from core.db.models import User
from core.services.tg_bot.user_tg_services import UserTgService


pytestmark = pytest.mark.anyio


async def test_create_user_and_get_by_tg_id(db_session):
    created = await UserTgService.create_user(db_session, tg_id=100, tg_nickname="nick100")
    await db_session.commit()

    assert isinstance(created, User)
    assert created.tg_id == 100
    assert created.tg_nickname == "nick100"

    fetched = await UserTgService.get_user_by_tg_id(db_session, tg_id=100)
    assert fetched.id == created.id


async def test_get_or_create_returns_existing(db_session):
    first = await UserTgService.create_user(db_session, tg_id=200, tg_nickname="nick200")
    await db_session.commit()

    second = await UserTgService.get_or_create_user(db_session, tg_id=200, tg_nickname="ignored")

    assert second.id == first.id
    assert second.tg_nickname == "nick200"


async def test_create_user_duplicate_raises(db_session):
    await UserTgService.create_user(db_session, tg_id=300, tg_nickname="nick300")
    await db_session.commit()

    with pytest.raises(ValueError):
        await UserTgService.create_user(db_session, tg_id=300, tg_nickname="nick300-again")
