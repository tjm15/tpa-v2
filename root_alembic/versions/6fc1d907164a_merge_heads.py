"""Merge heads

Revision ID: 6fc1d907164a
Revises: 78cc7b762d8b, e30a12487533
Create Date: 2025-05-26 17:30:38.082568

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6fc1d907164a'
down_revision = ('78cc7b762d8b', 'e30a12487533')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
