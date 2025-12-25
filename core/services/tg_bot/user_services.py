from core.db.session import async_session
from core.services.tg_bot.user_db_services import UserService
from core.db.models import User


session = async_session()

async def user_authentication(user_tg_id: int) -> User:
    try:
        async with session.begin():

            user = await UserService.get_user_by_tg_id(
                session,
                tg_id=user_tg_id
            )

            if not user:
                raise ValueError(f"User with Telegram ID {user_tg_id} not found")

            return user
    except Exception as e:
        raise print(f'Auth error: {e}')
    finally:
        await session.close()


async def user_authorization(user_tg_id: int, username: str) -> User:
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
