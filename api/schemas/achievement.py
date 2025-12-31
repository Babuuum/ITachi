from typing import Optional
from pydantic import Field

from api.schemas.base import BaseSchema


class AchievementBase(BaseSchema):
    name: str = Field(..., max_length=20, description="Название ачивки")
    description: Optional[str] = Field(None, description="Описание ачивки")
    difficult: str = Field(default="uncommon", description="Сложность ачивки")
    active: bool = Field(default=True, description="Статус ачивки")

class AchievementCreate(AchievementBase):
    pass


class AchievementUpdate(BaseSchema):
    name: Optional[str] = Field(None, max_length=20)
    description: Optional[str] = None
    difficult: Optional[str] = None
    active: Optional[bool] = None


class AchievementInDB(AchievementBase):
    id: int


class AchievementResponse(AchievementInDB):
    pass