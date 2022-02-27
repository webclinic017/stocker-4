import logging
from constant import Constant
import sys
import os
from logging.handlers import TimedRotatingFileHandler
from login import login


def initialize_log(file_name):
    """This Method Initialize the Logfile

    Args:
        file_name (str): Absolute Path of the Logfile
    """
    logger = logging.getLogger()
    logger = logging.getLogger()
    handler = TimedRotatingFileHandler(
        file_name, when='midnight', backupCount=5)
    formatter = logging.Formatter("%(asctime)s - [%(levelname)s] - "
                                  "[%(filename)s)] - [%(funcName)s] "
                                  "- [%(lineno)d] - %(message)s")
    handler.setFormatter(formatter)
    handler.setLevel(logging.INFO)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    logger.info("++++++++++++++++++++++++++++++++++++++++++++++++++++")
    logger.info('Starting The Application')
    logger.info("++++++++++++++++++++++++++++++++++++++++++++++++++++")


if not os.path.exists(Constant.DEPLOY_DIR):
    print("Deploy Directory " + Constant.DEPLOY_DIR +
          " does not exist. Exiting the app.")
    sys.exit(1)

if not os.path.exists(Constant.LOGFILE_DIR):
    print("Logfile Directory " + Constant.LOGFILE_DIR +
          " does not exist. Exiting the app.")
    sys.exit(1)

initialize_log(Constant.LOGFILE_DIR + "/startup.log")

kite = login()


logging.info(kite)
