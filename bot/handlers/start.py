from aiogram.filters import CommandStart
from aiogram import Router
from aiogram.types import Message

from core.services.tg_bot.user_services import user_auth

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    user_tg_id = message.from_user.id
    username = message.from_user.username

    user = await user_auth(user_tg_id=user_tg_id, username=username)

    await message.answer(
        f"Привет, {username}!\n"
        f"Статус: {'Активен' if user.is_active else 'Неактивен'}"
    )