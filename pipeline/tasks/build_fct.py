import logging

import luigi
from sqlalchemy import func, insert, select

from models.db import get_db_session
from models.models import CuratedFctProduct, StageSearchResultsScraped

from .build_dim import BuildDim

logger = logging.getLogger(__name__)


class BuildFctStatus(luigi.Target):
    def __init__(self, today: str):
        super().__init__()
        self.today = today

    def exists(self):
        status = 0
        query_stmt = (
            select(func.count(CuratedFctProduct.process_date))
            .where(CuratedFctProduct.process_date == self.today)
        )
        with get_db_session() as session:
            logger.debug(f"query generated to check records: {query_stmt}")
            status = session.execute(query_stmt).fetchone()[0]

        return True if status else False


class BuildFct(luigi.Task):
    today = luigi.Parameter()

    def requires(self):
        return BuildDim(today=self.today)

    def output(self):
        return BuildFctStatus(self.today)

    def run(self):
        logger.info(f"fact build started for {self.today}")

        try:
            insert_stmt = insert(CuratedFctProduct).from_select(
                [
                    "process_date",
                    "search_option_category",
                    "search_option_sort",
                    "product_id",
                    "product_mrp",
                    "product_price",
                    "product_discount",
                    "product_rating",
                    "product_rating_count"
                ],
                select(
                    StageSearchResultsScraped.process_date,
                    StageSearchResultsScraped.search_option_category,
                    StageSearchResultsScraped.search_option_sort,
                    StageSearchResultsScraped.product_id,
                    StageSearchResultsScraped.product_mrp,
                    StageSearchResultsScraped.product_price,
                    StageSearchResultsScraped.product_discount,
                    StageSearchResultsScraped.product_rating,
                    StageSearchResultsScraped.product_rating_count,
                )
                .where(StageSearchResultsScraped.process_date == self.today)
                .distinct(),
            )
            logger.debug(f"query generated to load records: {insert_stmt}")

            with get_db_session() as session:
                result = session.execute(insert_stmt)
                logger.info(f"loaded {result.rowcount} records into fct for {self.today}")

            logger.debug(f"data successfully loaded")

        except Exception:
            logger.exception(f"uncaught exception")
            raise

        logger.info(f"fact build completed for {self.today}")
