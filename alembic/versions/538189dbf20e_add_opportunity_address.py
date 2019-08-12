"""add_opportunity_address

Revision ID: 538189dbf20e
Revises: 013e93ffb94a
Create Date: 2019-08-11 16:22:27.853621

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '538189dbf20e'
down_revision = '013e93ffb94a'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('Opportunity', sa.Column('address', sa.String()))


def downgrade():
    op.drop_column('Opportunity', 'address')
