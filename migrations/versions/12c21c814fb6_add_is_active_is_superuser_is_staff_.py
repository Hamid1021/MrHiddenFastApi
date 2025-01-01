"""add is_active, is_superuser, is_staff, date_joined, last_login, is_owner to User Model

Revision ID: 12c21c814fb6
Revises: eca28d50aae7
Create Date: 2025-01-01 14:01:01.876061

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '12c21c814fb6'
down_revision: Union[str, None] = 'eca28d50aae7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Users', sa.Column('is_active', sa.Boolean(), nullable=True))
    op.add_column('Users', sa.Column('is_superuser', sa.Boolean(), nullable=True))
    op.add_column('Users', sa.Column('is_staff', sa.Boolean(), nullable=True))
    op.add_column('Users', sa.Column('date_joined', sa.DateTime(), nullable=True))
    op.add_column('Users', sa.Column('last_login', sa.DateTime(), nullable=True))
    op.add_column('Users', sa.Column('is_owner', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Users', 'is_owner')
    op.drop_column('Users', 'last_login')
    op.drop_column('Users', 'date_joined')
    op.drop_column('Users', 'is_staff')
    op.drop_column('Users', 'is_superuser')
    op.drop_column('Users', 'is_active')
    # ### end Alembic commands ###