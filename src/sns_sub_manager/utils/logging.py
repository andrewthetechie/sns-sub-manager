from functools import lru_cache
from logging import getLogger as _getLogger
from logging.config import dictConfig

from ..config import Config
from ..config import get_config


def setup_logger(config: Config):
    dictConfig(config.log_dict_config)


@lru_cache()
def get_logger():
    app_name = get_config().app_name
    return _getLogger(app_name)
