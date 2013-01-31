import logging
import sys

def init_log(log_level=logging.INFO, logger="libpepa"):
    logging.basicConfig(level=log_level, format="%(name)s:%(levelname)s:%(filename)s:%(funcName)s:%(lineno)d  -  %(message)s")
    log = logging.getLogger(logger)
    log.setLevel(log_level)
    return log
