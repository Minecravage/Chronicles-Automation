import logging
from logging.handlers import TimedRotatingFileHandler
import datetime

def create_logger():
    logger = logging.getLogger("app")
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "[%(levelname)s] %(asctime)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)

    # file_handler = TimedRotatingFileHandler(filename=f"logs/{datetime.date.today().strftime("%Y-%m-%d")}.log", when="d", interval=1, backupCount="5", encoding="utf8")
    # file_handler.setLevel(logging.INFO)
    # file_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    # logger.addHandler(file_handler)

    return logger