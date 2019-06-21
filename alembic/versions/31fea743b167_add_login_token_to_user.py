"""add login token to user

Revision ID: 31fea743b167
Revises: 47ef3050097f
Create Date: 2019-06-21 20:39:40.621625

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '31fea743b167'
down_revision = '47ef3050097f'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('User', sa.Column('login_token', sa.String()))
    op.add_column('User', sa.Column('login_token_expiration', sa.TIMESTAMP, server_default=sa.func.now()))


def downgrade():
    op.drop_column('User', 'login_token_expiration')
    op.drop_column('User', 'login_token')
