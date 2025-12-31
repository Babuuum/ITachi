from aiogram.filters import Command
from aiogram import Router
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from core.services.achievement_db_services import AchievementDbService
from core.utils.user_auth import user_auth

router = Router()


@router.message(Command('user_achievements'))
async def user_achievements(message: Message, session: AsyncSession):
    user = await user_auth(session=session, message=message)
    achievements = await AchievementDbService.get_achievements_for_user(session=session, user_id=user.id)

    if achievements == []:
        return await message.answer("У вас нет доступных достижений.")

    await message.answer(
        "Доступные достижения:\n" + "\n".join([f"- {ach.name}: {ach.description}" for ach in achievements]))
