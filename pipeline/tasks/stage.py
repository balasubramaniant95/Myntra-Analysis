import logging

import luigi
from sqlalchemy import delete, func, insert, select

from models.db import get_db_session
from models.models import LandingSearchResultsScraped, StageSearchResultsScraped

from .load import Load

logger = logging.getLogger(__name__)

class StageStatus(luigi.Target):
    def __init__(self, today: str):
        super().__init__()
        self.today = today

    def exists(self):
        status = 0
        query_stmt = (
            select(func.count(StageSearchResultsScraped.process_date))
            .where(StageSearchResultsScraped.process_date == self.today)
        )
        with get_db_session() as session:
            logger.debug(f"query generated to check records: {query_stmt}")
            status = session.execute(query_stmt).fetchone()[0]

        return True if status else False


class Stage(luigi.Task):
    today = luigi.Parameter()

    def requires(self):
        return Load(today=self.today)

    def output(self):
        return StageStatus(self.today)

    def run(self):
        logger.info(f"staging of data started for {self.today}")

        try:
            insert_stmt = insert(StageSearchResultsScraped).from_select(
                [
                    "process_date",
                    "search_option_category",
                    "search_option_sort",
                    "product_id",
                    "product_name",
                    "product_brand",
                    "product_search_image",
                    "product_gender",
                    "product_primary_colour",
                    "product_category",
                    "product_year",
                    "product_season",
                    "product_catalog_date",
                    "product_mrp",
                    "product_price",
                    "product_discount",
                    "product_rating",
                    "product_rating_count",
                ],
                select(
                    LandingSearchResultsScraped.process_date,
                    LandingSearchResultsScraped.search_option_category,
                    LandingSearchResultsScraped.search_option_sort,
                    LandingSearchResultsScraped.product_id,
                    LandingSearchResultsScraped.product_name,
                    LandingSearchResultsScraped.product_brand,
                    LandingSearchResultsScraped.product_search_image,
                    LandingSearchResultsScraped.product_gender,
                    LandingSearchResultsScraped.product_primary_colour,
                    LandingSearchResultsScraped.product_category,
                    LandingSearchResultsScraped.product_year,
                    LandingSearchResultsScraped.product_season,
                    LandingSearchResultsScraped.product_catalog_date,
                    LandingSearchResultsScraped.product_mrp,
                    LandingSearchResultsScraped.product_price,
                    LandingSearchResultsScraped.product_discount,
                    LandingSearchResultsScraped.product_rating,
                    LandingSearchResultsScraped.product_rating_count,
                ).distinct(),
            )
            logger.debug(f"query generated to load records: {insert_stmt}")
            
            with get_db_session() as session:
                result = session.execute(insert_stmt)
                logger.info(f"loaded {result.rowcount} records into stage for {self.today}")

            logger.debug(f"data successfully loaded")

        except Exception:
            logger.exception(f"uncaught exception")
            raise

        logger.info(f"staging of data completed for {self.today}")
