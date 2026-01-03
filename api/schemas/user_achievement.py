from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class UserAchievementBase(BaseModel):
    user_id: int
    achievement_id: int
    completed: bool = False
    completed_at: Optional[datetime] = None


class UserAchievementCreate(UserAchievementBase):
    pass


class UserAchievementUpdate(BaseModel):
    completed: Optional[bool] = None
    completed_at: Optional[datetime] = None


class UserAchievementResponse(UserAchievementBase):
    achievement_name: Optional[str] = None
    achievement_description: Optional[str] = None

    class Config:
        from_attributes = True


class AchievementWithStatus(BaseModel):
    id: int
    name: str
    description: Optional[str]
    difficult: str
    active: bool
    completed: bool
    completed_at: Optional[datetime]

    class Config:
        from_attributes = True