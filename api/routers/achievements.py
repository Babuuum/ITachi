from typing import List

from fastapi import APIRouter, status, HTTPException

from api.schemas.achievement import AchievementResponse, AchievementCreate, AchievementUpdate
from core.db.session import SessionDep
from core.services.achievement_db_services import AchievementDbService


router = APIRouter(prefix='/achievements', tags=['achievements'])

@router.get('/', response_model=List[AchievementResponse])
async def get_achievements(session: SessionDep):
    achievements_list =  await AchievementDbService.get_all_achievements(session)

    return achievements_list

@router.get('/by-name/{achievement_name}', response_model=AchievementResponse)
async def get_achievement_by_name(achievement_name: str, session: SessionDep):
    achievement =  await AchievementDbService.get_achievement_by_name(session, achievement_name)
    if not achievement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="achievement not found"
        )

    return achievement

@router.get('/{achievement_id}', response_model=AchievementResponse)
async def get_achievement_by_id(achievement_id: int, session: SessionDep):
    achievement =  await AchievementDbService.get_achievement_by_id(session, achievement_id)
    if not achievement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="achievement not found"
        )

    return achievement

@router.post('/',response_model=AchievementResponse, status_code=status.HTTP_201_CREATED)
async def create_achievement(achievement: AchievementCreate, session: SessionDep):
    new_achievement = await AchievementDbService.create_achievement(session, achievement)

    if not new_achievement:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="achievement name already exists",
        )

    return new_achievement

@router.put('/{achievement_id}',response_model=AchievementResponse)
async def update_achievement(achievement_id: int, achievement: AchievementUpdate, session: SessionDep):
    updated_achievement = await AchievementDbService.update_achievement(session, achievement_id, achievement)

    if not updated_achievement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="achievement not found",
        )

    return updated_achievement

@router.delete('/{achievement_id}')
async def delete_achievement(achievement_id: int, session: SessionDep):
    achievement_status =  await AchievementDbService.delete_achievement(session, achievement_id)

    if not achievement_status:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="achievement not found"
        )

    return {"status": "success", "message": "Achievement marked as inactive"}

@router.delete('/hard/{achievement_id}')
async def delete_achievement_hard(achievement_id: int, session: SessionDep):
    achievement_status =  await AchievementDbService.delete_achievement_hard(session, achievement_id)

    if not achievement_status:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="achievement not found"
        )

    return {"status": "success", "message": "Achievement deleted"}