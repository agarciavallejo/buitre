"""Initial schema

Revision ID: 47ef3050097f
Revises:
Create Date: 2019-02-13 20:36:28.176958

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '47ef3050097f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
    	'Comment',
    	sa.Column('id', sa.Integer, primary_key=True),
    	sa.Column('created_at', sa.DateTime),
    	sa.Column('updated_at', sa.DateTime),
    	sa.Column('last_updated_by', sa.String(16)),
    	sa.Column('opportunity_id', sa.Integer, sa.ForeignKey('Opportunity.id'), nullable=False),
    	sa.Column('user_id', sa.Integer, sa.ForeignKey('User.id'), nullable=False),
    	sa.Column('score', sa.Numeric)  # Score of the comment
    )

    op.create_table(
    	'CommentLike',
    	sa.Column('id', sa.Integer, primary_key=True),
    	sa.Column('created_at', sa.DateTime),
    	sa.Column('updated_at', sa.DateTime),
    	sa.Column('last_updated_by', sa.String(16)),
    	sa.Column('comment_id', sa.Integer, sa.ForeignKey('Comment.id'), nullable=False),
    	sa.Column('user_id', sa.Integer, sa.ForeignKey('User.id'), nullable=False),
    	sa.Column('score', sa.Numeric)  # Thumbs up / down ??
    )

    op.create_table(
    	'Opportunity',
    	sa.Column('id', sa.Integer, primary_key=True),
    	sa.Column('created_at', sa.DateTime),
    	sa.Column('updated_at', sa.DateTime),
    	sa.Column('last_updated_by', sa.String(16)),
    	sa.Column("name", sa.String),
    	sa.Column("description", sa.String),
    	sa.Column("latitude", sa.Numeric(9, 6)),
    	sa.Column("longitude", sa.Numeric(9, 6)),
    	sa.Column("score", sa.Numeric),
    	sa.Column("closing_date", sa.Date),
    	sa.Column("user_id", sa.Integer, sa.ForeignKey('User.id'), nullable=False),
    )

    op.create_table(
    	'OpportunityLike',
    	sa.Column('id', sa.Integer, primary_key=True),
    	sa.Column('created_at', sa.DateTime),
    	sa.Column('updated_at', sa.DateTime),
    	sa.Column('last_updated_by', sa.String(16)),
		sa.Column("opportunity_id", sa.Integer, sa.ForeignKey('Opportunity.id'), nullable=False),
    	sa.Column("user_id", sa.Integer, sa.ForeignKey('User.id'), nullable=False),
    	sa.Column("score", sa.Integer)  # ??
    )

    op.create_table(
    	'OpportunitySchedule',
    	sa.Column('id', sa.Integer, primary_key=True),
    	sa.Column('created_at', sa.DateTime),
    	sa.Column('updated_at', sa.DateTime),
    	sa.Column('last_updated_by', sa.String(16)),
    	sa.Column("start_time", sa.Time, nullable=False)
    	sa.Column("end_time", sa.Time, nullable=False)
    	sa.Column("monday", sa.Boolean)
    	sa.Column("tuesday", sa.Boolean)
    	sa.Column("wednesday", sa.Boolean)
    	sa.Column("thursday", sa.Boolean)
    	sa.Column("friday", sa.Boolean)
    	sa.Column("saturday", sa.Boolean)
    	sa.Column("sunday", sa.Boolean)
    	sa.Column("opportunity_id", sa.Integer, sa.ForeignKey('Opportunity.id'), nullable=False)
    )

    op.create_table(
    	'OpportunityTag',
    	sa.Column('id', sa.Integer, primary_key=True),
    	sa.Column('created_at', sa.DateTime),
    	sa.Column('updated_at', sa.DateTime),
    	sa.Column('last_updated_by', sa.String(16)),
    	sa.Column("opportunity_id", sa.Integer, sa.ForeignKey('Opportunity.id'), nullable=False, primary_key=True)
    	sa.Column("tag_id", sa.Integer, sa.ForeignKey('Tag.id'), nullable=False, primary_key=True)
    )

    op.create_table(
    	'Picture',
    	sa.Column('id', sa.Integer, primary_key=True),
    	sa.Column('created_at', sa.DateTime),
    	sa.Column('updated_at', sa.DateTime),
    	sa.Column('last_updated_by', sa.String(16)),
    	sa.Column("opportunity_id", sa.Integer, sa.ForeignKey('Opportunity.id'), nullable=False)
    	sa.Column('path', sa.String)
    )

    op.create_table(
    	'Tag',
    	sa.Column('id', sa.Integer, primary_key=True),
    	sa.Column('created_at', sa.DateTime),
    	sa.Column('updated_at', sa.DateTime),
    	sa.Column('last_updated_by', sa.String(16)),
    	sa.Column("name", sa.String)
    	sa.Column("tag_id", sa.Integer, sa.ForeignKey('Tag.id'))
    )

    op.create_table(
    	'User',
    	sa.Column('id', sa.Integer, primary_key=True),
    	sa.Column('created_at', sa.DateTime),
    	sa.Column('updated_at', sa.DateTime),
    	sa.Column('last_updated_by', sa.String(16)),
    	sa.Column("name", String)
    	sa.Column("email" String)
    	sa.Column('password', String)
    	sa.Column('latitude', sa.Numeric(9, 6))
    	sa.Column('longitude', sa.Numeric(9, 6))
    	sa.Column('radius', sa.Integer)
    	sa.Column('is_valid', sa.Boolean)
    	sa.Column('score', sa.Integer)
    )

    op.create_table(
    	'User',
    	sa.Column('id', sa.Integer, primary_key=True),
    	sa.Column('created_at', sa.DateTime),
    	sa.Column('updated_at', sa.DateTime),
    	sa.Column('last_updated_by', sa.String(16)),
    	sa.Column("tag_id", sa.Integer, sa.ForeignKey('Tag.id'), nullable=False)
		sa.Column("tag_id", sa.Integer, sa.ForeignKey('Tag.id'), nullable=False)
    )


def downgrade():
	op.drop_table('OpportunityTag')
	op.drop_table('OpportunitySchedule')
	op.drop_table('OpportunityLike')
	op.drop_table('Opportunity')
	op.drop_table('CommentLike')
    op.drop_table('Comment')
