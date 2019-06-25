"""add user validation token

Revision ID: a95648908a7b
Revises: 31fea743b167
Create Date: 2019-06-22 11:33:01.623914

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a95648908a7b'
down_revision = '31fea743b167'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('User', sa.Column('validation_token', sa.String()))
    op.add_column('User', sa.Column('validation_token_expiration', sa.TIMESTAMP, server_default=sa.func.now()))


def downgrade():
    op.drop_column('User', 'validation_token_expiration')
    op.drop_column('User', 'validation_token')
