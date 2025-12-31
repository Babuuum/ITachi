from aiogram.filters import CommandStart
from aiogram import Router
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from core.utils.user_auth import user_auth

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message, session: AsyncSession):
    username = message.from_user.username

    user = await user_auth(session=session, message=message)

    await message.answer(
        f"Привет, {username}!\n"
        f"Статус: {'Активен' if user.is_active else 'Неактивен'}"
    )
