"""add address and pin_code to youth and make youth_id nullable in attendance

Revision ID: ac4b29bca817
Revises: c999c6703807
Create Date: 2025-07-17 15:28:46.032149

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ac4b29bca817'
down_revision: Union[str, Sequence[str], None] = 'c999c6703807'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add address and pin_code columns to youths table
    op.add_column('youths', sa.Column('address', sa.VARCHAR(), nullable=True))
    op.add_column('youths', sa.Column('pin_code', sa.VARCHAR(), nullable=True))

    # Modify youth_id in attendances table to be nullable
    op.alter_column('attendances', 'youth_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    
def downgrade() -> None:
    """Downgrade schema."""
    # Remove added columns
    op.drop_column('youths', 'pin_code')
    op.drop_column('youths', 'address')
    
    # Revert youth_id to non-nullable
    op.alter_column('attendances', 'youth_id',
               existing_type=sa.INTEGER(),
               nullable=False)