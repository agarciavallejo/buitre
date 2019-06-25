"""rename login token and remove expirations

Revision ID: f5ca506eca29
Revises: a95648908a7b
Create Date: 2019-06-23 17:07:29.173319

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f5ca506eca29'
down_revision = 'a95648908a7b'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column('User', 'validation_token_expiration')
    op.drop_column('User', 'login_token_expiration')
    op.alter_column('User', 'login_token', new_column_name='session_token')


def downgrade():
    op.alter_column('User', 'session_token', new_column_name='login_token')
    op.add_column('User', sa.Column('login_token_expiration', sa.TIMESTAMP, server_default=sa.func.now()))
    op.add_column('User', sa.Column('validation_token_expiration', sa.TIMESTAMP, server_default=sa.func.now()))

