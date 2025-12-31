"""achievement_status

Revision ID: 4d3fec7deb2a
Revises: 6fe9a4379188
Create Date: 2025-12-31 04:42:44.990579

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4d3fec7deb2a'
down_revision: Union[str, Sequence[str], None] = '6fe9a4379188'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade() -> None:
    # 1) Добавляем колонку NOT NULL, но с server_default, чтобы старые строки не стали NULL
    op.add_column(
        "achievements",
        sa.Column(
            "active",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("true"),  # или "false", если нужно
        ),
    )

    # 2) Убираем дефолт на уровне БД (оставь, только если хочешь default именно в БД)
    op.alter_column("achievements", "active", server_default=None)

    # 3) Лучше дать явное имя constraint (а не None), чтобы downgrade был стабильным
    op.create_unique_constraint("uq_achievements_name", "achievements", ["name"])


def downgrade() -> None:
    op.drop_constraint("uq_achievements_name", "achievements", type_="unique")
    op.drop_column("achievements", "active")
