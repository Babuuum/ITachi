from fastapi import FastAPI

from api.routers.users import router as users_router
from api.routers.achievements import router as achievements_router

from bot.main import dp, bot


app = FastAPI(title='ITachi')

app.include_router(users_router)
app.include_router(achievements_router)


@app.on_event("startup")
async def on_startup():
    await dp.start_polling(bot)


@app.on_event("shutdown")
async def on_shutdown():
    await bot.session.close()