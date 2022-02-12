import logging

import luigi
from sqlalchemy import func, select

from config import config
from models.db import get_db_session
from models.models import LandingSearchResultsScraped

from .ingest import Ingest

logger = logging.getLogger(__name__)


class LoadStatus(luigi.Target):
    def __init__(self, today: str):
        super().__init__()
        self.today = today

    def exists(self):
        status = 0
        query_stmt = (
            select(func.count(LandingSearchResultsScraped.process_date))
            .where(LandingSearchResultsScraped.process_date == self.today)
        )
        with get_db_session() as session:
            logger.debug(f"query generated to check records: {query_stmt}")
            status = session.execute(query_stmt).fetchone()[0]

        return True if status else False


class Load(luigi.Task):
    today = luigi.Parameter()

    def requires(self):
        return Ingest(today=self.today)

    def output(self):
        return LoadStatus(self.today)

    def run(self):
        data_file = config.PROCESSING_DIR.joinpath(f"{self.today}.csv")
        if not data_file.is_file():
            logger.error("processed data file not found for loading")
            return None

        logger.info(f"data load started for {self.today}")

        try:
            with get_db_session() as session:
                cursor = session.connection().connection.cursor()

                with open(data_file, "r") as f:
                    cursor.copy_expert(
                        sql = f"""
                            copy {LandingSearchResultsScraped.__table_args__.get("schema") + "." + LandingSearchResultsScraped.__tablename__}(process_date, process_file, search_option_category, search_option_sort, product_id, product_name, product_brand, product_search_image, product_gender, product_primary_colour, product_category, product_year, product_season, product_catalog_date, product_mrp, product_price, product_discount, product_rating, product_rating_count)
                            from stdin
                            delimiter '|' csv;
                        """,
                        file=f,
                    )
                    logger.info(f"loaded {cursor.rowcount} records from data file {data_file.name}")

            logger.debug(f"data successfully loaded from file {data_file.name} into database")

        except Exception:
            logger.exception(f"uncaught exception")
            raise

        logger.info(f"data load completed for {self.today}")
