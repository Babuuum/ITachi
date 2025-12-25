from typing import List

from core.db.session import async_session
from core.db.models import Achievement
from core.services.tg_bot.achievement_db_services import AchievementService


session = async_session()

async def get_achievements() -> List[Achievement]:
    try:
        async with session.begin():
            achievements = await AchievementService.get_all_achievements(session)
            return achievements          

    except Exception as e:
        raise print(f'Auth error: {e}')
    finally:
        await session.close()
