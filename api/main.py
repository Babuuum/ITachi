import asyncio

from aiogram.types import Update
from fastapi import Depends, FastAPI, Request

from api.routers.achievements import router as achievements_router
from api.routers.user_achievements import router as user_achievements_router
from api.routers.users import router as users_router

from bot.main import dp, bot
from core.config import get_settings
from api.dependencies.auth import require_auth
from api.middlewares import AuthMiddleware


settings = get_settings()

app = FastAPI(title='ITachi')

app.add_middleware(
    AuthMiddleware,
    token=settings.API_TOKEN,
    exempt_paths={settings.webhook_endpoint},
)

app.include_router(users_router, dependencies=[Depends(require_auth)])
app.include_router(achievements_router, dependencies=[Depends(require_auth)])
app.include_router(user_achievements_router, dependencies=[Depends(require_auth)])

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
