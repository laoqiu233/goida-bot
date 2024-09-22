"""added chunks

Revision ID: 5b13da32d8b5
Revises: d082f563e1b4
Create Date: 2024-09-22 02:53:48.901440

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5b13da32d8b5'
down_revision: Union[str, None] = 'd082f563e1b4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('document_chunks',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('article_id', sa.Uuid(), nullable=False),
    sa.ForeignKeyConstraint(['article_id'], ['articles.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('document_chunks')
    # ### end Alembic commands ###
