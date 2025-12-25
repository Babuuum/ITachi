from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from core.db.models import Achievement, UserAchievement


class AchievementService:
    @staticmethod
    async def get_achievements_for_user(session: AsyncSession, user_id: int) -> List[Achievement]:
        achievement = await session.scalars(select(UserAchievement).where(UserAchievement.user_id == user_id, UserAchievement.completed == False))  # noqa: E712
        return achievement.all()
    
    @staticmethod
    async def get_all_achievements(session: AsyncSession) -> List[Achievement]:
        achievements = await session.scalars(select(Achievement))
        return achievements.all()

    @staticmethod
    async def add_achievement_to_user(session: AsyncSession, user_id: int, achievement_name: str) -> UserAchievement:
        achievement = await session.scalars(select(Achievement).where(Achievement.name == achievement_name))
        achievement = achievement.first()
        if not achievement:
            raise ValueError(f"Achievement with name {achievement_name} not found")
        user_achievement = UserAchievement(user_id=user_id, achievement_id=achievement.id)
        session.add(user_achievement)
        return user_achievement
