import logging
from logging.handlers import RotatingFileHandler
import sys

logger = logging.getLogger(__name__)


def init():
    init_logging()


def init_logging():
    """
    Initializes logging with handlers.
    """
    formatter = logging.Formatter("%(asctime)s %(levelname)8s --- [%(threadName)-8s] [%(filename)s:%(lineno)d] %(funcName)s: %(message)s")

    info_handler = logging.StreamHandler(sys.stdout)
    info_handler.setFormatter(formatter)
    # make it log less serious messages to stdout
    info_handler.addFilter(lambda record: record.levelno < logging.WARNING)

    error_handler = logging.StreamHandler(sys.stderr)
    error_handler.setFormatter(formatter)
    error_handler.setLevel(logging.WARNING)

    # maxBytes=1MB, backupCount=3 log file will be rotated after reaching 1MB, up to 3 backup files will be kept.
    file_handler = RotatingFileHandler('application.log', maxBytes=1024*1024, backupCount=3, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    logger.handlers = [info_handler, error_handler, file_handler]
    logger.setLevel(logging.DEBUG)

