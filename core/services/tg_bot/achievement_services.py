from typing import List, Sequence

from core.db.session import async_session
from core.db.models import Achievement, UserAchievement
from core.services.tg_bot.achievement_db_services import AchievementService


session = async_session()

async def get_achievements() -> List[Achievement]:
    try:
        async with session.begin():
            achievements = await AchievementService.get_all_achievements(session)
            return achievements          

    except Exception as e:
        raise print(f'get achievement error: {e}')
    finally:
        await session.close()

async def complete_achievement(user_id: int, achievement_name: str) -> None:
    try:
        async with session.begin():
            await AchievementService.add_achievement_to_user(session, user_id, achievement_name)

    except Exception as e:
        raise print(f'complete_achievement error: {e}')
    finally:
        await session.close()

async def get_user_achievements(user_id: int) -> Sequence[Achievement]:
    try:
        async with session.begin():
            achievements = await AchievementService.get_achievements_for_user(session, user_id)
            return achievements

    except Exception as e:
        raise print(f'get achievement error: {e}')
    finally:
        await session.close()

async def get_user_completed_achievements(user_id: int) -> Sequence[Achievement]:
    try:
        async with session.begin():
            achievements = await AchievementService.get_completed_achievements_for_user(session, user_id)
            return achievements

    except Exception as e:
        raise print(f'get achievement error: {e}')
    finally:
        await session.close()

async def achievement_check(achievement_name: str) -> bool:
    try:
        async with session.begin():
            achievement = await AchievementService.get_achievement_by_name(session, achievement_name)
            if achievement:
                return True
            else:
                return False

    except Exception as e:
        raise print(f'get achievement error: {e}')
    finally:
        await session.close()
