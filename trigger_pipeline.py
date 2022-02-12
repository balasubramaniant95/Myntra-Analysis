import logging.config

import luigi

from config import config
from pipeline.pipeline import Pipeline

logging.config.dictConfig(config.LOGGING_CONFIG_DICT)

if __name__ == "__main__":
    luigi.build(
        [Pipeline()],
        local_scheduler=True
    )
