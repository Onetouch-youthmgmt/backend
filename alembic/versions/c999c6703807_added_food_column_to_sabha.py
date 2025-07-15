"""added food column to sabha

Revision ID: c999c6703807
Revises: 
Create Date: 2025-07-15 15:31:20.813379

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'c999c6703807'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add the food column to the existing sabhas table
    op.add_column('sabhas', sa.Column('food', sa.String(), nullable=False, server_default=''))


def downgrade() -> None:
    """Downgrade schema."""
    # Remove the food column if we need to roll back
    op.drop_column('sabhas', 'food')