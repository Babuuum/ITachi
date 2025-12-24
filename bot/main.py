from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from bot.handlers.start import router as start_router
from bot.handlers.add_progress import router as add_progress_router
from bot.handlers.achievements import router as achievements_router

from core.config import get_settings

settings = get_settings()

bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

dp.include_router(start_router)
dp.include_router(add_progress_router)
dp.include_router(achievements_router)