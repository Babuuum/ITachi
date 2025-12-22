from datetime import datetime, timezone
from typing import Optional, List
from sqlalchemy import Integer, String, DateTime, TEXT, BOOLEAN, ForeignKey, Table, Column
from sqlalchemy.orm import mapped_column, Mapped, relationship
# from sqlalchemy import Enum as SQLEnum
# from enum import Enum

from app.core.db.base import Base


# class LeagueFormat(Enum):
#     CHILL = 'chill'  # duration 2 weeks
#     SOFT = 'soft'    # duration 1 month
#     NORMAL = 'normal' # duration 3 month


# class AchievementsDifficult(Enum):
#     COMMON = 'common'
#     UNCOMMON = 'uncommon'
#     RARE = 'rare'
#     EPIC = 'epic'
#     LEGENDARY = 'legendary'


league_goals = Table(
    "leagues_achievements",
    Base.metadata,
    Column('league_id', ForeignKey('leagues.id'), primary_key=True),
    Column('achievement_id', ForeignKey('achievements.id'), primary_key=True)
)

users_achievements = Table(
    "users_achievements",
    Base.metadata,
    Column('user_id', ForeignKey('users.id'), primary_key=True),
    Column('achievement_id', ForeignKey('achievements.id'), primary_key=True),
    Column('completed', BOOLEAN, default=False),
    Column('completed_at', DateTime, nullable=True)
)
#добавить classmethod, для формирования прогресс баров для сложных ачивок
#добавить функцию проверки выполнения условий для разблокировки и условий выполнения
#сделать трекинг лист ачивок

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tg_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True, unique=True)
    tg_nickname: Mapped[str] = mapped_column(String(100), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )
    is_active: Mapped[bool] = mapped_column(BOOLEAN, default=True)


    achievements: Mapped[List['Achievement']] = relationship(
        secondary="users_achievements",
        back_populates='users'
    )


class League(Base):
    __tablename__ = 'leagues'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(20), nullable=False)
    active: Mapped[bool] = mapped_column(BOOLEAN, default=False)
    ended: Mapped[bool] = mapped_column(BOOLEAN, default=False)

    start_league_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )

    format: Mapped[str] = mapped_column(String(15), default='normal')
    # format: Mapped[LeagueFormat] = mapped_column(
    #     SQLEnum(LeagueFormat),
    #     default=LeagueFormat.NORMAL,
    #     nullable=False
    # )

    achievements: Mapped[List['Achievement']] = relationship(
        secondary="leagues_achievements",
        back_populates='leagues'
    )


class Achievement(Base):
    __tablename__ = 'achievements'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(20), nullable=False)
    # achievement_group_id: Mapped[int | None] = mapped_column(ForeignKey("achievements.id"), nullable=True)
    # achievement_requirement_id: Mapped[int | None] = mapped_column(ForeignKey("achievements.id"), nullable=True)
    description: Mapped[Optional[str]] = mapped_column(TEXT, nullable=True)

    # achievement_group: Mapped['Achievement'] = relationship(
    #     back_populates='req_to_complite',
    #     remote_side=[id],
    #     foreign_keys=[achievement_group_id]
    #     )
    # req_to_complite: Mapped[List['Achievement']] = relationship(
    #     back_populates='achievement_group'
    # )

    # achievement_requirements: Mapped['Achievement'] = relationship(
    #     back_populates='req_to_unlock',
    #     remote_side=[id],
    #     foreign_keys=[achievement_requirement_id]
    #     )
    # req_to_unlock: Mapped[List['Achievement']] = relationship(
    #     back_populates='achievement_requirements'
    # )

    users: Mapped[List['User']] = relationship(
        secondary="users_achievements",
        back_populates='achievements'
    )
    leagues: Mapped[List[League]] = relationship(
        secondary="leagues_achievements",
        back_populates='achievements'
    )

    difficult: Mapped[str] = mapped_column(String(15), default='uncommon')
    # difficult: Mapped[AchievementsDifficult] = mapped_column(
    #     SQLEnum(AchievementsDifficult),
    #     default=AchievementsDifficult.UNCOMMON,
    #     nullable=False
    # )
