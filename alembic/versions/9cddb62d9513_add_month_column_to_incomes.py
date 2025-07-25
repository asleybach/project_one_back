"""Add month column to incomes

Revision ID: 9cddb62d9513
Revises: f005c141350e
Create Date: 2025-05-06 10:53:49.496133

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9cddb62d9513'
down_revision: Union[str, None] = 'f005c141350e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('expenses', sa.Column('month', sa.String(), nullable=False))
    op.add_column('incomes', sa.Column('month', sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('incomes', 'month')
    op.drop_column('expenses', 'month')
    # ### end Alembic commands ###
