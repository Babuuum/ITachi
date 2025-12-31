from aiogram.filters import Command
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy.ext.asyncio import AsyncSession

from core.services.achievement_db_services import AchievementDbService
from core.utils.user_auth import user_auth

router = Router()

class Achievement(StatesGroup):
    achievement = State()


@router.message(Command('complete_achievement'))
async def add_progress(message: Message,  state: FSMContext, session: AsyncSession):
    user = await user_auth(session=session, message=message)
    await state.update_data(user_id=user.id)
    await state.set_state(Achievement.achievement)
    await message.answer("Введите название ачивки")

@router.message(Achievement.achievement)
async def achievement_name(message: Message, state: FSMContext, session: AsyncSession):
    state_data = await state.get_data()
    user_id = state_data.get('user_id')

    if not user_id:
        await message.answer('Не удалось определить пользователя. Попробуйте снова.')
        await state.clear()
        return

    achievement_name = message.text
    achievement_exists = await AchievementDbService.get_achievement_by_name(session=session, achievement_name=achievement_name)

    if achievement_exists:
        await AchievementDbService.add_achievement_to_user(session=session, user_id=user_id, achievement_name=achievement_name)
        await message.answer('achievement complete')
    else:
        await message.answer('achievement not found')

    await state.clear()
