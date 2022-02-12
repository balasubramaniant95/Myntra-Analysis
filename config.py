from pathlib import Path
from urllib.parse import quote


class Config:
    BASE = Path(__file__).parent

    # dataset
    DATASET_DIR = BASE.joinpath("dataset")
    STAGE_DIR = DATASET_DIR.joinpath("stage")
    PROCESSING_DIR = DATASET_DIR.joinpath("processing")

    # app
    CATEGORY_OPTIONS = ["clothing", "accessories", "footwear", "myntra-fashion-store", "personal-care", "baby-care", "home-furnishing"]
    FILTER_OPTIONS = ["", "Gender:men,men women", "Gender:men women,women", "Gender:boys,boys girls", "Gender:boys girls,girls"]
    SORT_OPTIONS = ["recommended", "new", "popularity", "discount"]
    PAGE_LIMIT = 10

    # database
    DATABASE_NAME = <DATABASE_NAME>
    DATABASE_USER = <DATABASE_USER>
    DATABASE_PASSWD = quote(<DATABASE_PASSWD>)
    DATABASE_HOST = <DATABASE_HOST>
    DATABASE_PORT = <DATABASE_PORT>
    DATABASE_URI = f"postgresql+psycopg2://{DATABASE_USER}:{DATABASE_PASSWD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"

    # logging
    DEFAULT_LOG_LEVEL = "INFO"
    LOG_DIR = BASE.joinpath("logs")
    LOGGING_CONFIG_DICT = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "simple": {"format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"},
            "verbose": {"format": "%(asctime)s - %(name)s - %(threadName)s - %(module)s - %(funcName)s - %(levelname)s - %(message)s"},
        },
        "handlers": {
            "console": {
                "level": DEFAULT_LOG_LEVEL,
                "class": "logging.StreamHandler",
                "formatter": "simple",
            },
            "file": {
                "level": DEFAULT_LOG_LEVEL,
                "class": "logging.handlers.RotatingFileHandler",
                "formatter": "verbose",
                "filename": LOG_DIR.joinpath("app.log"),
                "maxBytes": 10 * (1024 ** 2),  # 10 MB
                "backupCount": 3,
            },
        },
        "loggers": {
            "root": {
                "handlers": ["console", "file"],
                "propagate": True,
                "level": "DEBUG",
            }
        },
    }


config = Config()
