"""create tables

Revision ID: 4881725b70dc
Revises: b42a2fb7ac9e
Create Date: 2024-08-29 12:03:52.282604

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4881725b70dc'
down_revision: Union[str, None] = 'b42a2fb7ac9e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('reservations', sa.Column('status', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('reservations', 'status')
    # ### end Alembic commands ###
