import shutil
import os

from logger import Logger

osp = os.path

# # debugging
# import time
# from datetime import datetime

class FileManager:
    DEFAULT_SPACE_RATE = 0.9
    logger = Logger()

    def __init__(self):
        self.dir_list = []              # directory paths to monitor
        self.drive_list = []
        self.max_space_rate = dict()
        self.auto_run = False
        self.interval = dict()

    def addDir(self, dir_path : str) -> bool:
        if not osp.isdir(dir_path):
            # print(f"%s not exists" %(dir_path))
            self.logger.warning(f"{dir_path} not exists")
            return False

        dir_list = self.dir_list
        dir_list_len = len(dir_list)

        dir_list.append(dir_path)

        if (dir_list_len + 1) != len(dir_list):
            # print(f"Failed to add dir : %s" %(dir_path))
            self.logger.warning(f"Failed to add dir : {dir_path}")
            return False
        
        drive = dir_path.split(":")[0] + ":"

        if drive not in self.drive_list:
            self.drive_list.append(drive)
            self.max_space_rate[drive] = self.DEFAULT_SPACE_RATE
    
        return True
    
    def removeDir(self, dir_path : str) -> bool:
        dir_list = self.dir_list
        dir_list_len = len(dir_list)

        if dir_path not in dir_list:
            self.logger.warning(f"{dir_path} not in directory list")
            return False

        dir_idx = dir_list.index(dir_path)
        removed_dir = dir_list.pop(dir_idx)

        
        if (dir_list_len - 1) != len(dir_list):
            # print(f"Failed to remove dir : %s" %(dir_path))
            self.logger.warning(f"Failed to remove dir : {dir_path}")
            return False

        # print(f"Remove monitoring directory : %s" %(removed_dir))
        self.logger.info(f"Monitoring directory removed : {removed_dir}")

        return True
    
    def setMaxSpaceRate(self, drive : str, rate : float) -> bool:
        if drive not in self.drive_list:
            self.logger.warning(f"{drive} is not in drive list")
            return False

        self.max_space_rate[drive] = rate

        self.logger.info(f"Set {drive} space rate to {rate}")

        return True

    def getMaxSpaceRate(self, drive : str) -> dict:
        if drive not in self.max_space_rate.keys():
            return -1
        
        return self.max_space_rate[drive]

    def getDirList(self) -> list:
        return self.dir_list
    
    def setDirList(self, dir_list : list) -> None:
        self.dir_list = dir_list

    def getDriveList(self) -> list:
        return self.drive_list
    
    def setDriveList(self, drive_list : list) -> None:
        self.drive_list = drive_list
    
    def getMaxSpaceRateDict(self):
        return self.max_space_rate
    
    def setMaxSpaceRateDict(self, max_space_rate_dict : dict) -> None:
        self.max_space_rate = max_space_rate_dict

    def isAutoRun(self):
        return self.auto_run
    
    def setAutoRun(self, is_auto_run):
        self.auto_run = is_auto_run

    def setIntervalDict(self, interval : dict):
        self.interval = interval

    def getIntervalDict(self):
        return self.interval
    
    def getConfig(self) -> dict:
        config = {}

        config["dir_list"] = self.getDirList()
        config["drive_list"] = self.getDriveList()
        config["max_space_rate"] = self.getMaxSpaceRateDict()
        config["auto_run"] = self.isAutoRun()
        config["interval"] = self.getIntervalDict()

        return config
    
    def setConfig(self, config : dict) -> None:
        self.setDirList(config["dir_list"])
        self.setDriveList(config["drive_list"])
        self.setMaxSpaceRateDict(config["max_space_rate"])
        self.setAutoRun(config["auto_run"])
        self.setIntervalDict(config["interval"])

    def deleteOldest(self, dir_path : str, delete_dir : bool) -> bool:
        if dir_path not in self.dir_list:
            self.logger.warning(f"{dir_path} is not in dir_list")
            return False
        
        space_threshold = -1

        for drive in self.drive_list:
            if drive in dir_path:
                space_threshold = self.max_space_rate[drive]
                break
        
        if space_threshold < 0:
            self.logger.info(f"Max space rate ({space_threshold}) is smaller than 0. Use setMaxSpaceRate.")
            return False

        self.logger.debug(f"_getUsageRate : {dir_path}")
        usage_rate = self._getUsageRate(dir_path)

        self.logger.debug(f"usage_rate : {usage_rate} / space_threshold : {space_threshold}")

        if usage_rate < space_threshold:
            return True

        oldest_path = self._getOldestPath(dir_path, delete_dir)
        
        if not oldest_path:
            self.logger.warning("There's no available oldest path")
            return True

        if osp.isdir(oldest_path):
            shutil.rmtree(oldest_path)
        elif osp.isfile(oldest_path):
            os.remove(oldest_path)
        else:
            self.logger.warning("Failed to delete. Not file or not directory")
            return False
        
        if osp.exists(oldest_path):
            self.logger.warning("Failed to delete.")
            return False
    
        # print("Finished to delete")
        self.logger.info(f"Finished to delete {oldest_path} : {osp.exists(oldest_path)}")

        return True
    
    def print(self):
        for dir_path in self.dir_list:
            for dir in os.listdir(dir_path):
                print(osp.join(dir_path, dir).replace("\\", "/"))

        return
    
    def _getOldestPath(self, dir_path : str, delete_dir : bool) -> str:
        if not osp.isdir(dir_path):
            self.logger.warning(f"{dir_path} does not exist")
            return ""
        
        self.logger.debug(f"search dir path : {dir_path}")
        path_list = []
        for dir in os.listdir(dir_path):
            self.logger.debug(dir)
            _dir_path = osp.join(dir_path, dir)

            if delete_dir and osp.isdir(_dir_path):
                path_list.append(osp.join(dir_path, dir)) #.replace("\\", "/"))
            
            if (not delete_dir) and (not osp.isdir(_dir_path)):
                path_list.append(osp.join(dir_path, dir)) #.replace("\\", "/"))

        if not path_list:
            self.logger.warning(f"No available paths in {dir_path}")
            return ""

        path_list.sort(key = lambda x: osp.getmtime(x))

        return path_list[0]
        
        debug_dir_list = [] # debug

        i = -1

        for dir in os.listdir(dir_path):

            dirr = osp.join(dir_path, dir)
            debug_dir_list.insert(0, dirr)  # debug

            modified_time = osp.getmtime(osp.join(dir_path, dir))
            print(dir, osp.isdir(osp.join(dir_path, dir)), " / ", modified_time, " / ", i < modified_time)
            i = modified_time
            # dt = datetime.strptime(modified_time, "%a %b %d %H:%M:%S %Y")
            # print(dt)

        debug_dir_pre_list_= debug_dir_list.copy()
        debug_dir_list.sort(key = lambda x: osp.getmtime(x))

        for dir_pre, dir in zip(debug_dir_pre_list_, debug_dir_list):
            print(dir_pre, dir)

        return
    
    def _getUsageRate(self, dir_path : str) -> float:
        if dir_path not in self.dir_list:
            self.logger.warning(f"{dir_path} not in dir list")
            return -1
        
        total, used, free = shutil.disk_usage(dir_path)
        total_gb, used_gb, free_gb = total / 2**30, used / 2**30, free / 2**30
        self.logger.info(f"Total : {total_gb:5.2f}GB, Used : {used_gb:5.2f}GB, Free : {free_gb:5.2f}GB")
        self.logger.debug(f"Space rate : {(used / total) * 100:5.2f}%")

        return used / total
