from aiogram.filters import Command
from aiogram import Router
from aiogram.types import Message


router = Router()

@router.message(Command('achievements'))
async def achievements(message: Message):
    ...