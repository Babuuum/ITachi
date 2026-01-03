from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from api.schemas.user_achievement import AchievementWithStatus, UserAchievementResponse
from core.db.models import Achievement, User, UserAchievement


class UserAchievementDbService:
    @staticmethod
    def _to_achievement_with_status(
        achievement: Achievement,
        ua: UserAchievement | None,
    ) -> AchievementWithStatus:
        return AchievementWithStatus(
            id=achievement.id,
            name=achievement.name,
            description=achievement.description,
            difficult=achievement.difficult,
            active=achievement.active,
            completed=bool(ua.completed) if ua else False,
            completed_at=ua.completed_at if ua else None,
        )

    @staticmethod
    async def get_user_achievements(session: AsyncSession, **kwargs) -> list[AchievementWithStatus] | None:
        user_id: int = kwargs["user_id"]
        completed: Optional[bool] = kwargs.get("completed")
        only_active_achievements: bool = kwargs.get("only_active_achievements", True)

        user = await session.scalar(select(User).where(User.id == user_id, User.is_active == True))
        if not user:
            return None

        stmt = (
            select(Achievement, UserAchievement)
            .outerjoin(
                UserAchievement,
                and_(
                    UserAchievement.achievement_id == Achievement.id,
                    UserAchievement.user_id == user_id,
                ),
            )
        )
        if only_active_achievements:
            stmt = stmt.where(Achievement.active == True)

        rows: list[tuple[Achievement, UserAchievement | None]] = (await session.execute(stmt)).all()
        items = [UserAchievementDbService._to_achievement_with_status(a, ua) for a, ua in rows]

        if completed is None:
            return items

        return [x for x in items if x.completed == completed]

    @staticmethod
    async def update_user_achievement(session: AsyncSession, **kwargs) -> UserAchievementResponse | None:
        user_id: int = kwargs["user_id"]
        achievement_id: int = kwargs["achievement_id"]
        completed: Optional[bool] = kwargs.get("completed")
        completed_at: Optional[datetime] = kwargs.get("completed_at")

        user = await session.scalar(select(User).where(User.id == user_id, User.is_active == True))
        if not user:
            return None

        achievement = await session.scalar(
            select(Achievement).where(Achievement.id == achievement_id, Achievement.active == True)
        )
        if not achievement:
            return None

        ua = await session.scalar(
            select(UserAchievement).where(
                UserAchievement.user_id == user_id,
                UserAchievement.achievement_id == achievement_id,
            )
        )
        if not ua:
            ua = UserAchievement(user_id=user_id, achievement_id=achievement_id, completed=False)
            session.add(ua)

        if completed is not None:
            ua.completed = completed
            if completed:
                ua.completed_at = completed_at or ua.completed_at or datetime.now(timezone.utc)
            else:
                ua.completed_at = None

        if completed_at is not None:
            ua.completed_at = completed_at

        await session.commit()
        await session.refresh(ua)

        return UserAchievementResponse(
            user_id=user_id,
            achievement_id=achievement_id,
            completed=ua.completed,
            completed_at=ua.completed_at,
            achievement_name=achievement.name,
            achievement_description=achievement.description,
        )

    @staticmethod
    async def remove_user_achievement(session: AsyncSession, **kwargs) -> bool:
        user_id: int = kwargs["user_id"]
        achievement_id: int = kwargs["achievement_id"]

        ua = await session.scalar(
            select(UserAchievement).where(
                UserAchievement.user_id == user_id,
                UserAchievement.achievement_id == achievement_id,
            )
        )
        if not ua:
            return False

        await session.delete(ua)
        await session.commit()
        return True
