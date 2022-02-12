import concurrent.futures
import csv
import datetime
import json
import logging
import os
import queue
import threading
import time
from pathlib import Path

import luigi

from config import config

from .scrape import Scrape

logger = logging.getLogger(__name__)
q = queue.Queue()


def write_to_csv(today):
    try:
        processing_dir = config.PROCESSING_DIR
        if not processing_dir.is_dir():
            processing_dir.mkdir(parents=True)
            logger.debug(f"{str(processing_dir)} did not exist. created required folder(s)")

        while not q.empty():
            time.sleep(1)
            continue

        with processing_dir.joinpath(f"{today}.csv").open("w", newline="") as file:
            writer = csv.writer(file, delimiter="|")
            while True:
                if q.empty():
                    time.sleep(2)
                    continue

                item = q.get()
                try:
                    writer.writerow(item)
                finally:
                    q.task_done()

    except Exception:
        logger.exception("uncaught exception")
        raise


def ingest_data(json_file: Path, base_path: Path, today: str):
    try:
        category, sort_option, _ = json_file.relative_to(base_path).parts

        with json_file.open("r") as j_file:
            products_data = json.load(j_file).get("products")
            if not products_data:
                logger.warning(f"products data is empty in file: {str(json_file)}")
                return None

            for product in products_data:
                row = [
                    today,
                    json_file.name,
                    category,
                    sort_option,
                    product.get("productId"),
                    product.get("productName"),
                    product.get("brand"),
                    product.get("searchImage"),
                    product.get("gender"),
                    product.get("primaryColour"),
                    product.get("category"),
                    product.get("year"),
                    product.get("season"),
                    datetime.datetime.fromtimestamp(int(product.get("catalogDate"))/1000).isoformat(),
                    product.get("mrp"),
                    product.get("price"),
                    product.get("discount"),
                    product.get("rating"),
                    product.get("ratingCount"),
                ]
                q.put(row)
            logger.debug(f"data successfully ingested from file: {json_file.name}")

    except (ValueError, AttributeError):
        logger.warning(f"failed to ingest data from file: {str(json_file)}", exc_info=True)

    except Exception:
        logger.exception(f"uncaught exception")
        raise


class Ingest(luigi.Task):
    today = luigi.Parameter()

    def requires(self):
        return Scrape(today=self.today)

    def output(self):
        return luigi.LocalTarget(config.PROCESSING_DIR.joinpath(f"{self.today}.csv"))

    def run(self):
        logger.info(f"data ingestion initiated for {self.today}")

        threading.Thread(target=write_to_csv, args=(self.today,), daemon=True).start()

        base_path = config.STAGE_DIR.joinpath(self.today)
        with concurrent.futures.ThreadPoolExecutor(max_workers=os.cpu_count()+4) as executor:
            for file in base_path.glob("**\*.json"):
                executor.submit(ingest_data, file, base_path, self.today)
                logger.debug(f"ingestion request submitted for file: {file}")

        q.join()
        logger.info(f"data ingestion completed for {self.today}")
