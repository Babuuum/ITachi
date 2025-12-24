from aiogram.filters import Command
from aiogram import Router
from aiogram.types import Message


router = Router()

@router.message(Command('add_progress'))
async def add_progress(message: Message):
    ...
    # dobavlenie achivki v progress
    # proverka na syshestvovanei achivki y usera
    # proverka na 3akritie