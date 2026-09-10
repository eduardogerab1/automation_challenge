import logging
import sys

def setup_logger():
    LOGGER_NAME = "automation_tests"
    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(logging.INFO)

    # Create a handler to print to the console
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    # Add the handler to the logger
    if not logger.handlers:
        logger.addHandler(handler)

    return logger

log = setup_logger()