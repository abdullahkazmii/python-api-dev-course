"""add foreign keys

Revision ID: a73f955f3035
Revises: 1c77065ebf0c
Create Date: 2024-09-30 16:06:40.089457

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a73f955f3035'
down_revision: Union[str, None] = '1c77065ebf0c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('Post',
                  sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table="Post", referent_table="users", local_cols=['owner_id'], remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade():
    op.drop_constraint('post_users_fk', table_name='Post')
    op.drop_column("Post", 'owner_id')
    pass
