"""alter tweets_party_parsed table name

Revision ID: 01cd2081c0e5
Revises: 65e56640cdae
Create Date: 2017-10-17 15:39:09.215000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '01cd2081c0e5'
down_revision = '65e56640cdae'
branch_labels = None
depends_on = None


def upgrade():
    op.rename_table('tweets_party_parsed','tweet_party_parsed')


def downgrade():
    pass
