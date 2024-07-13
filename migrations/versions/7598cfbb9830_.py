"""empty message

Revision ID: 7598cfbb9830
Revises: 1b1e898e96eb
Create Date: 2024-07-13 00:56:59.836029

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '7598cfbb9830'
down_revision: Union[str, None] = '1b1e898e96eb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('uesr', 'created_date')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('uesr', sa.Column('created_date', mysql.DATETIME(), nullable=False))
    # ### end Alembic commands ###
