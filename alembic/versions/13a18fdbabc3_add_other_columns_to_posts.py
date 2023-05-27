"""add other columns to posts

Revision ID: 13a18fdbabc3
Revises: 87540c071902
Create Date: 2023-05-26 16:46:41.886444

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '13a18fdbabc3'
down_revision = '87540c071902'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('published', sa.Boolean(),nullable=False, server_default='True'))
    op.add_column('posts', sa.Column('created_at',sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now')))

    pass


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'creted_at')

    pass
