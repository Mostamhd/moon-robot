from logging.config import dictConfig


def setup_logging():
    """Configure application logging"""
    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
            },
        },
        "root": {
            "level": "INFO",
            "handlers": ["console"],
        },
        "loggers": {
            "uvicorn": {
                "level": "INFO",
            },
            "sqlalchemy": {
                "level": "WARNING",
            },
            "robot": {
                "level": "DEBUG",
                "propagate": False,
                "handlers": ["console"],
            },
        },
    }

    dictConfig(logging_config)
