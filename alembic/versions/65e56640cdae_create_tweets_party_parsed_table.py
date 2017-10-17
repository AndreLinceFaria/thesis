"""Create tweets_party_parsed table

Revision ID: 65e56640cdae
Revises: 
Create Date: 2017-10-17 15:30:05.305000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '65e56640cdae'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'tweets_party_parsed',
        sa.Column('tweetId',sa.Integer, sa.ForeignKey('tweet.tweetId'), primary_key=True),
        sa.Column('username',sa.String, sa.ForeignKey('twitter_user.username')),
        sa.Column('text',sa.Text)
    )


def downgrade():
    pass
