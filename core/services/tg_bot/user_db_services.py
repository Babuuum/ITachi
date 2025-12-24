from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from core.db.models import User


class UserService:
    @staticmethod
    async def get_user_by_tg_id(session: AsyncSession, tg_id: int) -> User | None:
        result = await session.execute(select(User).where(User.tg_id == tg_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def create_user(session: AsyncSession, tg_id: int, tg_nickname: str) -> User:
        existing = await UserService.get_user_by_tg_id(session, tg_id)
        if existing:
            raise ValueError(f"User with Telegram ID {tg_id} already exists")

        user = User(tg_id=tg_id, tg_nickname=tg_nickname)
        session.add(user)
        return user

    @staticmethod
    async def get_or_create_user(session: AsyncSession, tg_id: int, tg_nickname: str) -> User:
        user = await UserService.get_user_by_tg_id(session, tg_id)
        if user:
            return user

        user = await UserService.create_user(session, tg_id, tg_nickname)
        return user