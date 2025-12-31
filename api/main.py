import asyncio

from aiogram.types import Update
from fastapi import FastAPI, Request

from api.routers.users import router as users_router
from api.routers.achievements import router as achievements_router

from bot.main import dp, bot
from core.config import get_settings


settings = get_settings()

app = FastAPI(title='ITachi')

app.include_router(users_router)
app.include_router(achievements_router)

@app.post(settings.webhook_endpoint)
async def telegram_webhook(request: Request):
    data = await request.json()
    update = Update(**data)
    await asyncio.sleep(1)
    await dp.feed_webhook_update(bot, update)
    return {"ok": True}

@app.on_event("startup")
async def on_startup():
    for attempt in range(1, 8):
        try:
            await bot.set_webhook(
                settings.webhook_url,
                allowed_updates=["message", "callback_query"]
            )

            return
        except Exception as e:
            print("set_webhook failed (attempt %s): %s", attempt, e)

        await asyncio.sleep(2 * attempt)

@app.on_event("shutdown")
async def on_shutdown():
    await bot.session.close()