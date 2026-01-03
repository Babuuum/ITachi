from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.types import Message

from core.services.tg_bot.user_tg_services import UserTgService
from core.db.models import User


async def user_auth(session: AsyncSession, message: Message) -> User:
    user_tg_id = message.from_user.id
    username = message.from_user.username
    user = await UserTgService.get_or_create_user(
        session,
        tg_id=user_tg_id,
        tg_nickname=username
    )
    return user
