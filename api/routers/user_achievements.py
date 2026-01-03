from typing import List, Optional

from fastapi import APIRouter, HTTPException, Query, status

from api.schemas.user_achievement import (
    AchievementWithStatus,
    UserAchievementResponse,
    UserAchievementUpdate,
)
from core.db.session import SessionDep
from core.services.user_achievement_db_services import UserAchievementDbService


router = APIRouter(prefix="/users/{user_id}/achievements", tags=["user_achievements"])


@router.get("/", response_model=List[AchievementWithStatus])
async def get_user_achievements(
    user_id: int,
    session: SessionDep,
    completed: Optional[bool] = Query(None, description="Фильтр по статусу выполнения"),
):
    res = await UserAchievementDbService.get_user_achievements(
        session=session,
        user_id=user_id,
        completed=completed,
    )
    if res is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
    return res


@router.get("/incomplete", response_model=List[AchievementWithStatus])
async def get_incomplete_achievements(user_id: int, session: SessionDep):
    res = await UserAchievementDbService.get_user_achievements(
        session=session,
        user_id=user_id,
        completed=False,
    )
    if res is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
    return res


@router.get("/completed", response_model=List[AchievementWithStatus])
async def get_completed_achievements(user_id: int, session: SessionDep):
    res = await UserAchievementDbService.get_user_achievements(
        session=session,
        user_id=user_id,
        completed=True,
    )
    if res is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
    return res


@router.put("/{achievement_id}", response_model=UserAchievementResponse)
async def update_user_achievement(
    user_id: int,
    achievement_id: int,
    data: UserAchievementUpdate,
    session: SessionDep,
):
    res = await UserAchievementDbService.update_user_achievement(
        session=session,
        user_id=user_id,
        achievement_id=achievement_id,
        **data.model_dump(exclude_unset=True),
    )
    if res is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user or achievement not found",
        )
    return res


@router.post("/{achievement_id}", response_model=UserAchievementResponse)
async def add_achievement_to_user(user_id: int, achievement_id: int, session: SessionDep):
    res = await UserAchievementDbService.update_user_achievement(
        session=session,
        user_id=user_id,
        achievement_id=achievement_id,
        completed=True,
    )
    if res is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user or achievement not found",
        )
    return res


@router.delete("/{achievement_id}")
async def remove_achievement_from_user(user_id: int, achievement_id: int, session: SessionDep):
    ok = await UserAchievementDbService.remove_user_achievement(
        session=session,
        user_id=user_id,
        achievement_id=achievement_id,
    )
    if not ok:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user achievement not found",
        )
    return {"status": "success", "message": "achievement removed from user"}
