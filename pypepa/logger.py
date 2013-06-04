import logging
import sys

_levels = {"INFO": logging.INFO, "DEBUG": logging.DEBUG, "ERROR" :logging.ERROR}
logger = None

def init_log(log_level="NONE", logger_name="pypepa"):
    global logger
    if logger is not None:
        return logger
    if log_level == "NONE":
        logging.basicConfig(level=logging.INFO,
                        format="%(name)s:%(levelname)s:%(filename)s: %(funcName)s:%(lineno)d  -  %(message)s")
        log = logging.getLogger(logger_name)
        log.setLevel(logging.INFO)
        log.disabled = True
        logger = log
    else:
        logging.basicConfig(level=_levels[log_level],
                        format="%(name)s:%(levelname)s:%(filename)s: %(funcName)s:%(lineno)d  -  %(message)s")
        log = logging.getLogger(logger_name)
        log.setLevel(log_level)
        logger = log
    return log
