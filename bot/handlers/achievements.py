from aiogram.filters import Command
from aiogram import Router
from aiogram.types import Message

from core.services.tg_bot.achievement_services import get_achievements
from core.services.tg_bot.user_services import user_authentication


router = Router()

@router.message(Command('achievements'))
async def achievements(message: Message):
    user_tg_id = message.from_user.id
    user = await user_authentication(user_tg_id=user_tg_id)

    if user is None:
        await message.answer("Пользователь не найден или не активен.")
        return
    
    achievements = await get_achievements()

    await message.answer("Доступные достижения:\n" + "\n".join([f"- {ach.name}: {ach.description}" for ach in achievements]))

    if achievements == []:
        await message.answer("У вас нет доступных достижений.")
