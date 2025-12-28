from typing import List, Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from core.db.models import Achievement
from core.services.achievement_db_services import AchievementDbService


async def get_achievements(session: AsyncSession) -> List[Achievement]:
    achievements = await AchievementDbService.get_all_achievements(session)
    return achievements


async def complete_achievement(session: AsyncSession, user_id: int, achievement_name: str) -> None:
    await AchievementDbService.add_achievement_to_user(session, user_id, achievement_name)


async def get_user_achievements(session: AsyncSession, user_id: int) -> Sequence[Achievement]:
    achievements = await AchievementDbService.get_achievements_for_user(session, user_id)
    return achievements


async def get_user_completed_achievements(session: AsyncSession, user_id: int) -> Sequence[Achievement]:
    achievements = await AchievementDbService.get_completed_achievements_for_user(session, user_id)
    return achievements


async def achievement_check(session: AsyncSession, achievement_name: str) -> bool:
    achievement = await AchievementDbService.get_achievement_by_name(session, achievement_name)
    return bool(achievement)
