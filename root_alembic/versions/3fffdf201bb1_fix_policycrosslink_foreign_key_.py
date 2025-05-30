"""Fix PolicyCrossLink foreign key constraints to CASCADE

Revision ID: 3fffdf201bb1
Revises: 6fc1d907164a
Create Date: 2025-05-26 17:30:44.948658

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3fffdf201bb1'
down_revision: Union[str, None] = '6fc1d907164a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # First, drop the existing foreign key constraints
    op.drop_constraint('policy_cross_links_source_policy_id_fkey', 'policy_cross_links', type_='foreignkey')
    op.drop_constraint('policy_cross_links_target_policy_id_fkey', 'policy_cross_links', type_='foreignkey')
    
    # Add the foreign key constraints back with CASCADE
    op.create_foreign_key(
        'policy_cross_links_source_policy_id_fkey',
        'policy_cross_links', 'policies',
        ['source_policy_id'], ['id'],
        ondelete='CASCADE'
    )
    op.create_foreign_key(
        'policy_cross_links_target_policy_id_fkey', 
        'policy_cross_links', 'policies',
        ['target_policy_id'], ['id'],
        ondelete='CASCADE'
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Drop the CASCADE constraints
    op.drop_constraint('policy_cross_links_source_policy_id_fkey', 'policy_cross_links', type_='foreignkey')
    op.drop_constraint('policy_cross_links_target_policy_id_fkey', 'policy_cross_links', type_='foreignkey')
    
    # Add the foreign key constraints back with SET NULL
    op.create_foreign_key(
        'policy_cross_links_source_policy_id_fkey',
        'policy_cross_links', 'policies',
        ['source_policy_id'], ['id'],
        ondelete='SET NULL'
    )
    op.create_foreign_key(
        'policy_cross_links_target_policy_id_fkey',
        'policy_cross_links', 'policies', 
        ['target_policy_id'], ['id'],
        ondelete='SET NULL'
    )
