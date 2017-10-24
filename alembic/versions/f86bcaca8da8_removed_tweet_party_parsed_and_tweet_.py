"""removed tweet_party_parsed and tweet_parsed tables

Revision ID: f86bcaca8da8
Revises: 01cd2081c0e5
Create Date: 2017-10-24 12:32:30.275000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f86bcaca8da8'
down_revision = '01cd2081c0e5'
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    op.drop_table('tweet_parsed')
    op.drop_table('tweet_party_parsed')
