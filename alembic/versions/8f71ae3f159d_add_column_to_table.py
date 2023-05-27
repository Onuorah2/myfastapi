"""add column to table

Revision ID: 8f71ae3f159d
Revises: f14d65c2483f
Create Date: 2023-05-26 15:31:22.063067

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8f71ae3f159d'
down_revision = 'f14d65c2483f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False ))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
