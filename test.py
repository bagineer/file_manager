import file_manager
import logging
import warnings

from logger import Logger

def main():
    

    # logger = logging.getLogger(__name__)
    # LOG_FORMAT = "[%(asctime)s.%(msecs)03d %(filename)s(%(lineno)s) - %(funcName)s] [%(levelname)s] %(message)s"
    # # LOG_FORMAT = "%(asctime)s:%(levelname)s:%(message)s"
    # DATE_FORMAT = "%Y/%m/%d %H:%M:%S"
    # logging.basicConfig(filename = "./test_log.log", format = LOG_FORMAT, datefmt = DATE_FORMAT, level = logging.DEBUG)

    # file_handler = logging.FileHandler("./test_log.log")
    # logger.addHandler(file_handler)

    # for i in range(100):
    #     logger.debug("debug")
    #     logger.info("info")
    #     logger.warning("warning")
    #     logger.error("error")
    #     logger.critical("critical")


    logger = Logger()
    logger.info("created")


if __name__ == "__main__":
    # fm = file_manager.FileManager()
    # result = fm.addDir("C:/CMES_SHELL")
    # result = fm.addDir("C:/CMES_PIXEL")
    # result = fm.addDir("C:/CMES_PIXELl")
    # result = fm.addDir("C:/CMES_PIXEL")

    # dir_path = "C:/CMES_SHELL/product/cmes3d/log/old"
    # result = fm.addDir(dir_path)

    # usage_rate = fm._getUsageRate(dir_path)
    # print("result :", result)
    # print("usage_rate :", usage_rate)

    # # fm.print()

    # print(fm.min_mtime_list[dir_path])
    
    # print(fm.deleteOldest(dir_path, delete_dir=False))

    # print(fm.min_mtime_list[dir_path])


    main()