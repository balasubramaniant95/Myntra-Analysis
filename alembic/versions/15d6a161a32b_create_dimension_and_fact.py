"""create dimension and fact

Revision ID: 15d6a161a32b
Revises: c9311744ef3c
Create Date: 2022-02-11 21:49:44.152019

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "15d6a161a32b"
down_revision = "c9311744ef3c"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "dim_product",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("product_id", sa.String, primary_key=True, index=True),
        sa.Column("product_name", sa.Text),
        sa.Column("product_brand", sa.String),
        sa.Column("product_search_image", sa.Text),
        sa.Column("product_gender", sa.String),
        sa.Column("product_primary_colour", sa.String),
        sa.Column("product_category", sa.String),
        sa.Column("product_year", sa.String),
        sa.Column("product_season", sa.String),
        sa.Column("product_catalog_date", sa.Date),
        sa.Column("created_date", sa.Date),
        schema="curated",
    )

    op.create_table(
        "fct_product",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("process_date", sa.String, index=True),
        sa.Column("search_option_category", sa.String),
        sa.Column("search_option_sort", sa.String),
        sa.Column("product_id", sa.String),
        sa.Column("product_mrp", sa.Float),
        sa.Column("product_price", sa.Float),
        sa.Column("product_discount", sa.Float),
        sa.Column("product_rating", sa.Float),
        sa.Column("product_rating_count", sa.Integer),
        schema="curated",
    )


def downgrade():
    op.drop_table("dim_product", schema="curated")
    op.drop_table("fct_product", schema="curated")
