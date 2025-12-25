import pytest
from sqlalchemy import select

from core.db.models import (
    Achievement,
    League,
    LeagueAchievement,
    User,
    UserAchievement,
)


pytestmark = pytest.mark.anyio


async def test_league_and_achievement_link(db_session):
    league = League(name="League1", active=True)
    achievement = Achievement(name="Ach1", difficult="common")

    league.achievements.append(achievement)
    db_session.add(league)
    await db_session.commit()

    refreshed = await db_session.get(League, league.id)
    assert refreshed.achievements[0].name == "Ach1"

    achievement_refetched = await db_session.get(Achievement, achievement.id)
    assert achievement_refetched.leagues[0].name == "League1"

    # Ensure association table has the link
    stmt = select(LeagueAchievement).where(
        LeagueAchievement.league_id == league.id,
        LeagueAchievement.achievement_id == achievement.id,
    )
    link = (await db_session.execute(stmt)).scalar_one()
    assert link.league_id == league.id
    assert link.achievement_id == achievement.id


async def test_user_achievement_cascade(db_session):
    user = User(tg_id=999, tg_nickname="cascade-user")
    ach = Achievement(name="AchCascade", difficult="rare")
    ua = UserAchievement(user=user, achievement=ach, completed=True)

    db_session.add_all([user, ach, ua])
    await db_session.commit()

    stmt = select(UserAchievement)
    before_delete = (await db_session.execute(stmt)).scalars().all()
    assert len(before_delete) == 1

    await db_session.delete(user)
    await db_session.commit()

    after_delete = (await db_session.execute(stmt)).scalars().all()
    assert after_delete == []
