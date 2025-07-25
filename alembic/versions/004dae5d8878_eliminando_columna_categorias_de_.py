"""Eliminando columna categorias de Ingresos

Revision ID: 004dae5d8878
Revises: 23e7c46cccd2
Create Date: 2025-05-26 15:17:26.105296

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '004dae5d8878'
down_revision: Union[str, None] = '23e7c46cccd2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('incomes', 'category')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('incomes', sa.Column('category', sa.VARCHAR(), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
