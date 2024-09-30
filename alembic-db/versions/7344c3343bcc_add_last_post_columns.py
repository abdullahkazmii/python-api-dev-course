"""add last Post Columns

Revision ID: 7344c3343bcc
Revises: a73f955f3035
Create Date: 2024-09-30 16:12:58.033534

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7344c3343bcc'
down_revision: Union[str, None] = 'a73f955f3035'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column("Post",
                  sa.Column("publish", sa.Boolean(), nullable=False, server_default='TRUE'),)
    op.add_column("Post",
                  sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')),)
    pass


def downgrade():
    op.drop_column("Post", 'publish')
    op.drop_column("Post", 'created_at')
    pass
