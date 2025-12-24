from core.db.session import async_session
from core.services.tg_bot.user_db_services import UserService
from core.db.models import User


session = async_session()

async def user_auth(user_tg_id: int, username: str) -> User:
    try:
        async with session.begin():

            user = await UserService.get_or_create_user(
                session,
                tg_id=user_tg_id,
                tg_nickname=username
            )

            return user
    except Exception as e:
        raise print(f'Auth error: {e}')
    finally:
        await session.close()
