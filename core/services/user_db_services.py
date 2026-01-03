from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Sequence

from core.db.models import User

class UserDbServices:
    @staticmethod
    async def get_all_users(session: AsyncSession) -> List[User]:
        users = await session.scalars(select(User))
        return users.all()


    @staticmethod
    async def get_user_by_name(session: AsyncSession, username: str) -> User | None:
        user = await session.scalars(select(User).where(User.tg_nickname == username))
        return user.first()


    @staticmethod
    async def get_user_by_id(session: AsyncSession, user_id: int) -> User | None:
        user = await session.scalars(select(User).where(User.id == user_id))
        return user.first()


    @staticmethod
    async def create_user(session: AsyncSession, data) -> User | None:
        user = User(**data.model_dump())
        session.add(user)
        try:
            await session.commit()
        except IntegrityError:
            await session.rollback()
            return None

        await session.refresh(user)
        return user


    @staticmethod
    async def update_user(session: AsyncSession, user_id: int, data) -> User | None:
        user = await UserDbServices.get_user_by_id(session, user_id)
        if not user:
            return None

        await session.execute(
            update(User).where(User.id == user_id).values(**data.model_dump(exclude_unset=True))
        )
        await session.commit()
        await session.refresh(user)
        return user


    @staticmethod
    async def delete_user(session: AsyncSession, user_id: int) -> bool:
        user = await UserDbServices.get_user_by_id(session, user_id)
        if not user:
            return False

        user.is_active = False
        await session.commit()
        return True


    @staticmethod
    async def delete_user_hard(session: AsyncSession, user_id: int) -> bool:
        user = await UserDbServices.get_user_by_id(session, user_id)
        if not user:
            return False

        await session.delete(user)
        await session.commit()
        return True