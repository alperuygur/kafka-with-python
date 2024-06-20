import logging
from colorlog import ColoredFormatter

LOG_FORMAT = (
    "%(log_color)s%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s"
)

def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Create a console handler and set the formatter
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # Define the color scheme
    formatter = ColoredFormatter(
        LOG_FORMAT,
        log_colors={
            'DEBUG': 'blue',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'magenta'
        }
    )
    ch.setFormatter(formatter)
    if not logger.handlers:
        logger.addHandler(ch)

    return logger
