import pytest
from sqlalchemy import select

from core.db.models import Achievement, User, UserAchievement
from core.services.tg_bot.achievement_db_services import AchievementService


pytestmark = pytest.mark.anyio


async def test_get_all_achievements(db_session):
    ach1 = Achievement(name="AchOne", description="first")
    ach2 = Achievement(name="AchTwo", description="second")
    db_session.add_all([ach1, ach2])
    await db_session.commit()

    achievements = await AchievementService.get_all_achievements(db_session)

    assert len(achievements) == 2
    names = {ach.name for ach in achievements}
    assert names == {"AchOne", "AchTwo"}


async def test_get_achievements_for_user(db_session):
    user = User(tg_id=42, tg_nickname="ach-user")
    ach = Achievement(name="AchUser", description="desc")
    user_ach = UserAchievement(user=user, achievement=ach, completed=False)
    db_session.add_all([user, ach, user_ach])
    await db_session.commit()

    result = await AchievementService.get_achievements_for_user(db_session, user_id=user.id)

    assert len(result) == 1
    assert result[0].user_id == user.id
    assert result[0].achievement_id == ach.id


async def test_add_achievement_to_user(db_session):
    user = User(tg_id=99, tg_nickname="adder")
    ach = Achievement(name="AddMe", description="desc")
    db_session.add_all([user, ach])
    await db_session.commit()

    created = await AchievementService.add_achievement_to_user(db_session, user_id=user.id, achievement_name="AddMe")
    await db_session.commit()

    assert created.user_id == user.id
    assert created.achievement_id == ach.id

    stmt = select(UserAchievement).where(UserAchievement.user_id == user.id, UserAchievement.achievement_id == ach.id)
    db_entry = (await db_session.execute(stmt)).scalar_one_or_none()
    assert db_entry is not None
