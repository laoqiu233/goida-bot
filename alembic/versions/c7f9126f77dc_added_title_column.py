"""Added title column

Revision ID: c7f9126f77dc
Revises: b3bcb536b9ef
Create Date: 2024-09-24 01:01:29.579488

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c7f9126f77dc'
down_revision: Union[str, None] = 'b3bcb536b9ef'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('articles', sa.Column('title', sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('articles', 'title')
    # ### end Alembic commands ###
