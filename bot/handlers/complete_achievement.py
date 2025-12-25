from aiogram.filters import Command
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup


from core.services.tg_bot.achievement_services import complete_achievement, achievement_check
from core.services.tg_bot.user_services import user_authentication

router = Router()

user_data_storage = {}

class Achievement(StatesGroup):
    achievement = State()


@router.message(Command('complete_achievement'))
async def add_progress(message: Message,  state: FSMContext):
    user_tg_id = message.from_user.id
    user = await user_authentication(user_tg_id)

    if user is None:
        await message.answer("Пользователь не найден или не активен.")
        return

    user_data_storage['user_id'] = user.id

    await state.set_state(Achievement.achievement)
    await message.answer("Введите название ачивки")

@router.message(Achievement.achievement)
async def achievement_name(message: Message, state: FSMContext):
    achievement_name = message.text
    achievement_exists = await achievement_check(achievement_name)

    if achievement_exists:
        await complete_achievement(user_data_storage['user_id'], achievement_name)
        await message.answer('achievement complete')
    else:
        await message.answer('achievement not found')

    await state.clear()
