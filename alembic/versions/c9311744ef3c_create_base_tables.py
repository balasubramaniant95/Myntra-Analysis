"""create base tables

Revision ID: c9311744ef3c
Revises: 7d432efd0cea
Create Date: 2022-02-05 11:25:19.016345

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "c9311744ef3c"
down_revision = "7d432efd0cea"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "search_results_scraped",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("process_date", sa.String),
        sa.Column("process_file", sa.String),
        sa.Column("search_option_category", sa.String),
        sa.Column("search_option_sort", sa.String),
        sa.Column("product_id", sa.String),
        sa.Column("product_name", sa.Text),
        sa.Column("product_brand", sa.String),
        sa.Column("product_search_image", sa.Text),
        sa.Column("product_gender", sa.String),
        sa.Column("product_primary_colour", sa.String),
        sa.Column("product_category", sa.String),
        sa.Column("product_year", sa.Integer),
        sa.Column("product_season", sa.String),
        sa.Column("product_catalog_date", sa.Date),
        sa.Column("product_mrp", sa.Float),
        sa.Column("product_price", sa.Float),
        sa.Column("product_discount", sa.Float),
        sa.Column("product_rating", sa.Float),
        sa.Column("product_rating_count", sa.Integer),
        schema="landing",
    )

    op.create_table(
        "search_results_scraped",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("process_date", sa.String),
        sa.Column("search_option_category", sa.String),
        sa.Column("search_option_sort", sa.String),
        sa.Column("product_id", sa.String),
        sa.Column("product_name", sa.Text),
        sa.Column("product_brand", sa.String),
        sa.Column("product_search_image", sa.Text),
        sa.Column("product_gender", sa.String),
        sa.Column("product_primary_colour", sa.String),
        sa.Column("product_category", sa.String),
        sa.Column("product_year", sa.String),
        sa.Column("product_season", sa.String),
        sa.Column("product_catalog_date", sa.Date),
        sa.Column("product_mrp", sa.Float),
        sa.Column("product_price", sa.Float),
        sa.Column("product_discount", sa.Float),
        sa.Column("product_rating", sa.Float),
        sa.Column("product_rating_count", sa.Integer),
        schema="stage",
    )


def downgrade():
    op.drop_table("search_results_scraped", schema="landing")
    op.drop_table("search_results_scraped", schema="stage")
