# this file sets the logging settings across all parts of the program
import logging

logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter("%(levelname)-8s%(module)s.%(funcName)s(): %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)