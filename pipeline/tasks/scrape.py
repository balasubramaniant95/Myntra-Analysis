import concurrent.futures
import json
import logging
import os
import re
from itertools import product

import luigi
import requests
from bs4 import BeautifulSoup

from config import config

logger = logging.getLogger(__name__)


def scrape_html(url: str, params: dict, timeout=30):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36"
    }

    response = requests.request("GET", url, headers=headers, params=params, timeout=timeout)
    if not response.status_code == 200:
        logger.warning(f"error requesting {url} for {params}: resp. status_code: {response.status_code}")
        return None

    try:
        soup = BeautifulSoup(response.text.encode("utf8"), "html.parser")
        for tag in soup.findAll("script", text=re.compile("searchData")):
            try:
                json_data = (
                    json.loads(tag.string.split(" = ")[1])
                    .get("searchData")
                    .get("results")
                )
                logger.debug(f"successfully scraped search results from {url} for {params}")
                return json_data

            except (IndexError, TypeError, AttributeError):
                logger.warning(f"unable to parse data from {url} for {params}", exc_info=True)
                continue
        
        logger.error(f"no search results from {url} for {params} to scrape")
        return None

    except Exception:
        logger.exception("uncaught exception")
        raise


class ScrapeStatus(luigi.Target):
    def __init__(self, today: str):
        super().__init__()
        self.today = today

    def exists(self):
        status = {}
        status_file = config.STAGE_DIR.joinpath("scrape.json")
        if status_file.is_file():
            with open(status_file, "r") as f:
                status = json.load(f)

        return True if status.get(self.today) == "Completed" else False


class Scrape(luigi.Task):
    today = luigi.Parameter()

    def output(self):
        return ScrapeStatus(self.today)

    def run(self):
        stage_dir = config.STAGE_DIR.joinpath(self.today)
        if not stage_dir.is_dir():
            stage_dir.mkdir(parents=True)
            logger.debug(f"{str(stage_dir)} did not exist. created required folder(s)")

        page_limit_options = list(range(1, config.PAGE_LIMIT+1))
        parameter_options = [
            config.CATEGORY_OPTIONS,
            config.FILTER_OPTIONS,
            config.SORT_OPTIONS,
            page_limit_options
        ]

        logger.info(f"scraping started for {self.today}")
        with concurrent.futures.ThreadPoolExecutor(max_workers=os.cpu_count() + 4) as executor:
            futures = {}
            for idx, opt in enumerate(product(*parameter_options)):
                url = "https://www.myntra.com/" + opt[0]
                params = {"f": opt[1], "sort": opt[2], "p": opt[3]}
                futures[executor.submit(scrape_html, url, params, 30)] = {
                    "category": opt[0],
                    "sort": opt[2],
                    "page": opt[3],
                    "idx": idx,
                }
                logger.debug(f"scrape request submitted for {url} with {params}")

            for future in concurrent.futures.as_completed(futures):
                meta = futures[future]
                try:
                    save_dir = stage_dir.joinpath(meta.get("category"), meta.get("sort"))
                    if not save_dir.is_dir():
                        save_dir.mkdir(parents=True)
                        logger.debug(f"{str(save_dir)} did not exist. created required folder(s)")

                    data = future.result()

                    if data and isinstance(data, dict):
                        out_file = f"search_results_{meta.get('page')}_{meta.get('idx')}.json"
                        with save_dir.joinpath(out_file).open("w") as j_file:
                            json.dump(data, j_file)
                            logger.debug(f"scraped search results dumped to {j_file.name}")
                    else:
                        logger.warning(f"search result data is empty or null or not of type 'dict' for {meta}: {data}")
                        continue

                except requests.ConnectTimeout:
                    logger.warning(f"scrape request timed out for {meta}", exc_info=True)

                except Exception:
                    logger.exception("uncaught exception")
                    raise

        logger.info(f"scraping completed for {self.today}")

        status_file = config.STAGE_DIR.joinpath("scrape.json")
        with open(status_file, "w") as f:
            status = json.load(f)
            status[self.today] = "Completed"
            json.dump(status, f)
