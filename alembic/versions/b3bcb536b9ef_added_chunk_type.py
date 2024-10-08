"""Added chunk type

Revision ID: b3bcb536b9ef
Revises: 5b13da32d8b5
Create Date: 2024-09-23 23:09:43.053458

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b3bcb536b9ef'
down_revision: Union[str, None] = '5b13da32d8b5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('document_chunks', sa.Column('chunk_type', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('document_chunks', 'chunk_type')
    # ### end Alembic commands ###
