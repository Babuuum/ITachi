from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Sequence

from core.db.models import Achievement, UserAchievement


class AchievementDbService:
    @staticmethod
    async def get_achievements_for_user(session: AsyncSession, user_id: int) -> Sequence[Achievement]:
        stmt = (
            select(Achievement)
            .join(UserAchievement, UserAchievement.achievement_id == Achievement.id)
            .where(
                UserAchievement.user_id == user_id,
                UserAchievement.completed == False
            )
        )
        achievements = await session.scalars(stmt)
        return achievements.all()


    @staticmethod
    async def get_completed_achievements_for_user(session: AsyncSession, user_id: int) -> Sequence[Achievement]:
        stmt = (
            select(Achievement)
            .join(UserAchievement, UserAchievement.achievement_id == Achievement.id)
            .where(
                UserAchievement.user_id == user_id,
                UserAchievement.completed == True
            )
        )
        achievements = await session.scalars(stmt)
        return achievements.all()

    @staticmethod
    async def add_achievement_to_user(session: AsyncSession, user_id: int, achievement_name: str) -> UserAchievement:
        achievement = await session.scalars(select(Achievement).where(Achievement.name == achievement_name))
        achievement = achievement.first()
        if not achievement:
            raise ValueError(f"Achievement with name {achievement_name} not found")
        user_achievement = UserAchievement(user_id=user_id, achievement_id=achievement.id, completed=True)
        session.add(user_achievement)
        return user_achievement
    
    @staticmethod
    async def get_all_achievements(session: AsyncSession) -> List[Achievement]:
        achievements = await session.scalars(select(Achievement))
        return achievements.all()

    @staticmethod
    async def get_achievement_by_name(session: AsyncSession, achievement_name: str) -> Achievement | None:
        achievement = await session.scalars(select(Achievement).where(Achievement.name == achievement_name))
        return achievement.first()

    @staticmethod
    async def get_achievement_by_id(session: AsyncSession, achievement_id: int) -> Achievement | None:
        achievement = await session.scalars(select(Achievement).where(Achievement.id == achievement_id))
        return achievement.first()

    @staticmethod
    async def create_achievement(session: AsyncSession, data) -> Achievement | None:
        achievement = Achievement(**data.model_dump())
        session.add(achievement)
        try:
            await session.commit()
        except IntegrityError:
            await session.rollback()
            return None

        await session.refresh(achievement)
        return achievement

    @staticmethod
    async def update_achievement(session: AsyncSession, achievement_id: int, data) -> Achievement | None:
        achievement = await AchievementDbService.get_achievement_by_id(session, achievement_id)
        if not achievement:
            return None

        await session.execute(
            update(Achievement).where(Achievement.id == achievement_id).values(**data.model_dump(exclude_unset=True))
        )
        await session.commit()
        await session.refresh(achievement)
        return achievement

    @staticmethod
    async def delete_achievement(session: AsyncSession, achievement_id: int) -> bool:
        achievement = await AchievementDbService.get_achievement_by_id(session, achievement_id)
        if not achievement:
            return False

        achievement.active = False
        await session.commit()
        return True

    @staticmethod
    async def delete_achievement_hard(session: AsyncSession, achievement_id: int) -> bool:
        achievement = await AchievementDbService.get_achievement_by_id(session, achievement_id)
        if not achievement:
            return False

        await session.delete(achievement)
        await session.commit()
        return True
