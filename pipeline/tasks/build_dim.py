import logging

import luigi
from sqlalchemy import delete, func, insert, select

from models.db import get_db_session
from models.models import CuratedDimProduct, StageSearchResultsScraped

from .stage import Stage

logger = logging.getLogger(__name__)


class BuildDimStatus(luigi.Target):
    def __init__(self, today: str):
        super().__init__()
        self.today = today

    def exists(self):
        status = 0
        query_stmt = (
            select(func.count(CuratedDimProduct.created_date))
            .where(CuratedDimProduct.created_date == self.today)
        )
        with get_db_session() as session:
            logger.debug(f"query generated to check records: {query_stmt}")
            status = session.execute(query_stmt).fetchone()[0]

        return True if status else False


class BuildDim(luigi.Task):
    today = luigi.Parameter()

    def requires(self):
        return Stage(today=self.today)

    def output(self):
        return BuildDimStatus(self.today)

    def run(self):
        logger.info(f"dimension build started for {self.today}")

        try:
            delete_stmt = (
                delete(CuratedDimProduct)
                .where(
                    CuratedDimProduct.product_id.in_(
                        select(StageSearchResultsScraped.product_id).where(
                            StageSearchResultsScraped.process_date == self.today
                        )
                    )
                )
                .execution_options(synchronize_session="fetch")
            )
            logger.debug(f"query generated to delete records: {delete_stmt}")

            insert_stmt = insert(CuratedDimProduct).from_select(
                [
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
                    "created_date",
                ],
                select(
                    StageSearchResultsScraped.product_id,
                    StageSearchResultsScraped.product_name,
                    StageSearchResultsScraped.product_brand,
                    StageSearchResultsScraped.product_search_image,
                    StageSearchResultsScraped.product_gender,
                    StageSearchResultsScraped.product_primary_colour,
                    StageSearchResultsScraped.product_category,
                    StageSearchResultsScraped.product_year,
                    StageSearchResultsScraped.product_season,
                    StageSearchResultsScraped.product_catalog_date,
                    func.to_date(self.today, 'YYYY-MM-DD'),
                )
                .where(StageSearchResultsScraped.process_date == self.today)
                .distinct(),
            )
            logger.debug(f"query generated to load records: {insert_stmt}")

            with get_db_session() as session:
                result = session.execute(delete_stmt)
                logger.info(f"deleted {result.rowcount} records from dim for {self.today}")

                result = session.execute(insert_stmt)
                logger.info(f"loaded {result.rowcount} records into dim for {self.today}")

            logger.debug(f"data successfully loaded")

        except Exception:
            logger.exception(f"uncaught exception")
            raise

        logger.info(f"dimension build started for {self.today}")

