import logging
from datetime import datetime

class Logger(logging.Logger):
    LOG_FORMAT = "[%(asctime)s.%(msecs)03d %(filename)s(%(lineno)s) %(funcName)s] [%(levelname)s] %(message)s"
    DATE_FORMAT = "%Y/%m/%d %H:%M:%S"

    def __init__(self):
        super().__init__(__name__)

        log_file_name = datetime.now().strftime('./%Y%m%d_log.log')
        file_handler = logging.FileHandler(filename = log_file_name)
        file_handler.setLevel(logging.DEBUG)

        formatter = logging.Formatter(fmt = self.LOG_FORMAT, datefmt = self.DATE_FORMAT)
        file_handler.setFormatter(formatter)

        self.addHandler(file_handler)



def main():
    logger = logging.getLogger(__name__)
    LOG_FORMAT = "[%(asctime)s %(filename)s(%(lineno)s) - %(funcName)s] [%(levelname)s] %(message)s"
    # LOG_FORMAT = "%(asctime)s:%(levelname)s:%(message)s"
    DATE_FORMAT = "%Y/%m/%d %H:%M:%S"
    logging.basicConfig(filename = "./test_log.log", format = LOG_FORMAT, datefmt = DATE_FORMAT, level = logging.DEBUG)

    file_handler = logging.FileHandler("./test_log.log")
    logger.addHandler(file_handler)

    logger.debug("debug")
    logger.info("info")
    logger.warning("warning")
    logger.error("error")
    logger.critical("critical")


if __name__ == "__main__":
    main()