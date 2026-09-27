"""test

Revision ID: 1168ae495714
Revises: 1ea9065121b3
Create Date: 2026-09-27 15:16:23.557136

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1168ae495714'
down_revision: Union[str, Sequence[str], None] = '1ea9065121b3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
