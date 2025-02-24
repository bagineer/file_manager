import file_manager
import threading
import time

from logger import Logger

class Worker(threading.Thread):
    logger = Logger()

    def __init__(self, name : str):
        super().__init__()
        self.name = name
        self.fm = None
        self.is_running = False
        self.interval_sec = 60

    def setFileManager(self, fm : file_manager.FileManager) -> None:
        self.fm = fm

    def run(self) -> None:
        try:
            if self.fm is None:
                self.logger.warning(f"File manager object not exist")
                return
            
            while True:
                if self.isRunning():
                    self.logger.info("is running...")

                    for dir_path in self.fm.getDirList():
                        if not self.isRunning():
                            break
                        
                        deleted = self.fm.deleteOldest(dir_path, delete_dir=False)
                        # deleted = False

                        if not deleted:
                            self.logger.warning(f"Failed to delete {dir_path}")
                else:
                    pass

                time.sleep(self.interval_sec)


        except Exception as e:
            self.logger.error("Running Error :", e)

    def rerun(self) -> None:
        if self.isRunning():
            return
        
        self.is_running = True
        self.logger.info("Start monitoring...")

    def stop(self) -> None:
        if not self.isRunning():
            return
        
        self.is_running = False
        self.logger.info("Stop monitoring...")

    def isRunning(self) -> bool:
        return self.is_running
    
    def setInterval(self, interval_sec : int):
        self.interval_sec = interval_sec


def main():
    fm = file_manager.FileManager()

    # dir_path = "C:/CMES_SHELL/product/cmes3d/log/old"
    # result = fm.addDir(dir_path)
    # result = fm.setMaxSpaceRate("C:", 0.982)

    worker = Worker("file_manager")
    worker.setFileManager(fm)

    worker.daemon = True
    worker.start()

    time.sleep(10)

# set daemon
# start

if __name__ == "__main__":
    main()