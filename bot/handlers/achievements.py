from aiogram.filters import Command
from aiogram import Router
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from core.services.tg_bot.achievement_services import get_achievements
from core.services.tg_bot.user_services import user_auth


router = Router()

@router.message(Command('achievements'))
async def achievements(message: Message, session: AsyncSession):
    await user_auth(session=session, message=message)
    achievements = await get_achievements(session=session)

    if achievements == []:
        return await message.answer("У вас нет доступных достижений.")

    await message.answer("Все достижения:\n" + "\n".join([f"- {ach.name}: {ach.description}" for ach in achievements]))
