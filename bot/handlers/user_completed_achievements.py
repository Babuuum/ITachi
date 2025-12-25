from aiogram.filters import Command
from aiogram import Router
from aiogram.types import Message

from core.services.tg_bot.achievement_services import get_user_completed_achievements
from core.services.tg_bot.user_services import user_authentication

router = Router()


@router.message(Command('user_completed_achievements'))
async def user_completed_achievements(message: Message):
    user_tg_id = message.from_user.id
    user = await user_authentication(user_tg_id=user_tg_id)

    if user is None:
        await message.answer("Пользователь не найден или не активен.")
        return

    achievements = await get_user_completed_achievements(user.id)
    if achievements == []:
        return await message.answer("У вас нет доступных достижений.")

    await message.answer(
        "Полученные достижения:\n" + "\n".join([f"- {ach.name}: {ach.description}" for ach in achievements]))
