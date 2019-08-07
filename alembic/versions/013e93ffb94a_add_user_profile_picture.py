"""add_user_profile_picture

Revision ID: 013e93ffb94a
Revises: f5ca506eca29
Create Date: 2019-08-07 18:19:53.448975

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '013e93ffb94a'
down_revision = 'f5ca506eca29'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('User', sa.Column('profile_picture', sa.String()))


def downgrade():
    op.drop_column('User', 'profile_picture')

