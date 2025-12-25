from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from bot.handlers.start import router as start_router
from bot.handlers.complete_achievement import router as complete_achievement_router
from bot.handlers.achievements import router as achievements_router
from bot.handlers.user_achievements import router as user_achievements_router
from bot.handlers.user_completed_achievements import router as user_completed_achievements_router

from core.config import get_settings

settings = get_settings()

bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

dp.include_router(start_router)
dp.include_router(complete_achievement_router)
dp.include_router(achievements_router)
dp.include_router(user_achievements_router)
dp.include_router(user_completed_achievements_router)