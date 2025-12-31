from aiogram.filters import Command
from aiogram import Router
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from core.services.achievement_db_services import AchievementDbService
from core.utils.user_auth import user_auth


router = Router()

@router.message(Command('achievements'))
async def achievements(message: Message, session: AsyncSession):
    await user_auth(session=session, message=message)
    achievements = await AchievementDbService.get_all_achievements(session=session)

    if achievements == []:
        return await message.answer("Нет доступных достижений.")

    await message.answer("Все достижения:\n" + "\n".join([f"- {ach.name}: {ach.description}" for ach in achievements]))
