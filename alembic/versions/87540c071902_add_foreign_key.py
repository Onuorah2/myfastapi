"""add foreign key

Revision ID: 87540c071902
Revises: 67411761f83d
Create Date: 2023-05-26 16:27:21.917785

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '87540c071902'
down_revision = '67411761f83d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk', source_table='posts', referent_table='users', local_cols=['owner_id'], remote_cols=['id'], ondelete='CASCADE')#remote cols is the users id
    pass


def downgrade() -> None:
    op.drop_constraint('posts_users_fk', table_name='posts')
    op.drop_column('posts', 'owner_id')
    pass
