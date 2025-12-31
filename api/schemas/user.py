from datetime import datetime
from typing import Optional
from pydantic import Field

from api.schemas.base import BaseSchema


class UserBase(BaseSchema):
    tg_id: int = Field(..., description="Telegram ID пользователя")
    tg_nickname: str = Field(..., max_length=100, description="Telegram никнейм")


class UserCreate(UserBase):
    pass


class UserUpdate(BaseSchema):
    tg_nickname: Optional[str] = Field(None, max_length=100)
    is_active: Optional[bool] = None


class UserInDB(UserBase):
    id: int
    created_at: datetime
    is_active: bool


class UserResponse(UserInDB):
    pass