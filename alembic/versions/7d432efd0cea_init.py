"""init

Revision ID: 7d432efd0cea
Revises: 
Create Date: 2022-01-22 10:55:49.531228

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "7d432efd0cea"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.execute("create schema landing")
    op.execute("create schema stage")
    op.execute("create schema curated")


def downgrade():
    op.execute("drop schema landing")
    op.execute("drop schema stage")
    op.execute("drop schema curated")
