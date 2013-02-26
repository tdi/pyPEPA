import logging
import sys

_levels = {"INFO": logging.INFO, "DEBUG": logging.DEBUG, "ERROR" :logging.ERROR} 

def init_log(log_level="INFO", logger="libpepa"):
    logging.basicConfig(level=_levels[log_level],
                        format="%(name)s:%(levelname)s:%(filename)s: %(funcName)s:%(lineno)d  -  %(message)s")
    log = logging.getLogger(logger)
    log.setLevel(log_level)
    return log
