"""create post table

Revision ID: afc908930447
Revises: 
Create Date: 2024-09-30 13:35:12.394927

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'afc908930447'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("Post", sa.Column('id', sa.Integer(), nullable = False, primary_key = True), sa.Column('title', sa.String(), nullable = False))


def downgrade() -> None:
    pass
