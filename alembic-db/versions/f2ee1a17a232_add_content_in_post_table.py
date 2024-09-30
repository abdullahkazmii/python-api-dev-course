"""add content in  post table

Revision ID: f2ee1a17a232
Revises: afc908930447
Create Date: 2024-09-30 15:39:18.497411

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f2ee1a17a232'
down_revision: Union[str, None] = 'afc908930447'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("Post", sa.Column('content', sa.String(), nullable = False))


def downgrade():
    op.drop_column("Post", 'content')
    pass
