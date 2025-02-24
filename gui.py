from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import tkinter.messagebox as msg

import file_manager
import thread
from utils import *
from logger import Logger

import os.path as osp
import json

# Button
#  - Set max space rateImport Config
#  - Export config
#  - Add directory
#  - Remove Directory
#  - Run monitoring
#  - Stop monitoring
#  - Set interval
# Label
#  - Drive
#  - Limit(Rate(%))
#  - Directories
#  - Interval
# Text
#  - Limit(Rate(%))
#  - Interval
# ComboBox
#  - Drive
# ListBox
#  - Directories
# CheckButton
#  - Auto run

class App(Tk):
    logger = Logger()

    def __init__(self):
        super().__init__()

        self.fm = None
        self.worker = None
        self.initial_dir = "./"

        self._init()
        self._init_ui()
        self.run()

    def _init(self) -> None:
        # thread
        self.fm = file_manager.FileManager()
        self.worker = thread.Worker("file_manager")
        self.worker.setFileManager(self.fm)

        self.worker.daemon = True
        # self.worker.start()

        ## Load config file
        # self.loadConfig("C:/Users/User/Desktop/cfg.json")
        self.loadConfig()

    def _init_ui(self) -> None:
        self.logger.info("_init_ui started.")

        self.title("File Manager")
        self.geometry("800x600")
        self.minsize(800, 600)
        self.configure(background="#DDDDDD")
        self.columnconfigure(0, weight=1)

        ############### Config ###############
        fr_top = Frame(self)
        # fr_config.grid(row = 0, column = 0, padx = 10, pady = 10, sticky = "EW")
        fr_top.pack(fill = "both", ipadx = 15, ipady = 15)

        # Label(fr_config, text = "", width = 1, height = 1).pack(side = "left", padx = 20)    # blank space

        # export config
        btn_export_cfg = Button(fr_top, command=self.exportConfig, width=10, height=1, text="Export", background = "#AAAAAA")
        btn_export_cfg.bind("<Enter>", lambda event : self._on_enter(self, btn_export_cfg))
        btn_export_cfg.bind("<Leave>", lambda event : self._on_leave(self, btn_export_cfg))
        btn_export_cfg.pack(side = "right", padx = 20)
        
        # import config
        btn_import_cfg = Button(fr_top, command=self.importConfig, width=10, height=1, text="Import", background = "#AAAAAA")
        btn_import_cfg.bind("<Enter>", lambda event : self._on_enter(self, btn_import_cfg))
        btn_import_cfg.bind("<Leave>", lambda event : self._on_leave(self, btn_import_cfg))
        btn_import_cfg.pack(side = "right")

        ############### Drive ###############
        # fr_drive = Frame(self)
        # # fr_drive.grid(row = 1, column = 0, padx = 10, pady = 10, sticky = "EW")
        # fr_drive.pack(fill = "both", ipadx = 15, ipady = 15)

        # select drive
        Label(fr_top, text = "Drive : ", height = 1).pack(side = "left", padx = (20, 0))
        self.cb_drive = ttk.Combobox(fr_top, width=5, height=15, values=[], state="readonly")
        self.cb_drive.bind("<<ComboboxSelected>>", self.showMaxSpaceRate)
        self.cb_drive.pack(side = "left", padx = (0, 20))

        # show drive max space rate
        Label(fr_top, text = "Max Space : ", height = 1).pack(side = "left", padx = (20, 0))
        self.txt_max_space_rate = Text(fr_top, width=5, height=1)
        self.txt_max_space_rate.pack(side = "left")
        Label(fr_top, text = "%", height = 1).pack(side = "left", padx = 10)

        # set max space rate
        btn_set_rate = Button(fr_top, command=self.setMaxSpaceRate, width=10, height=1, text="Set", background = "#AAAAAA")
        btn_set_rate.bind("<Enter>", lambda event : self._on_enter(self, btn_set_rate))
        btn_set_rate.bind("<Leave>", lambda event : self._on_leave(self, btn_set_rate))
        btn_set_rate.pack(side = "left", padx = 20)
        
        ############### Directories ###############
        fr_dirs = Frame(self)
        # fr_dirs.grid(row = 2, column = 0, padx = 10, pady = 10, sticky = "NSEW")
        fr_dirs.pack(fill = "both", expand = True, ipadx = 15, ipady = 15)

        fr_dirs_1 = Frame(fr_dirs)
        fr_dirs_1.pack(fill = "x", ipadx = 15, ipady = 15)

        fr_dirs_2 = Frame(fr_dirs)
        fr_dirs_2.pack(fill = "both", expand = True, ipadx = 15, ipady = 15)
        
        # Remove directory
        btn_remove_dir = Button(fr_dirs_1, command=self.removeDir, width=10, height=1, text="Remove", background = "#AAAAAA")
        btn_remove_dir.bind("<Enter>", lambda event : self._on_enter(self, btn_remove_dir))
        btn_remove_dir.bind("<Leave>", lambda event : self._on_leave(self, btn_remove_dir))
        btn_remove_dir.pack(side = "right", padx = 20)

        # Add directory
        Label(fr_dirs_1, text = "Monitoring directories ", height = 1).pack(side = "left", padx = 20)
        btn_add_dir = Button(fr_dirs_1, command=self.addDir, width=10, height=1, text="Add", background = "#AAAAAA")
        btn_add_dir.bind("<Enter>", lambda event : self._on_enter(self, btn_add_dir))
        btn_add_dir.bind("<Leave>", lambda event : self._on_leave(self, btn_add_dir))
        btn_add_dir.pack(side = "right")

        # show directory list
        self.list_dirs = Listbox(fr_dirs_2, height=0, selectmode="single")
        self.list_dirs.pack(anchor = "n", padx = 20, fill = "both", expand = True)

        ############### Execute ###############
        fr_exe = Frame(self)
        # fr_exe.grid(row = 3, column = 0, padx = 10, pady = 10, sticky = "ES")
        fr_exe.pack(fill = "both", ipadx = 15, ipady = 15)

        # Auto run
        self.chk_var_auto_run = IntVar()
        self.chk_auto_run = ttk.Checkbutton(fr_exe, text = "Auto Run", command = self.onClickCheckButton, variable = self.chk_var_auto_run)
        # self.chk_auto_run.bind("<Button-1><ButtonRelease-1>", self.onClickCheckButton)
        self.chk_auto_run.pack(side = "left", anchor = "w", padx = (20, 0))

        # Show interval
        Label(fr_exe, text = "Interval : ", height = 1).pack(side = "left", padx = (20, 0))
        self.txt_interval = Text(fr_exe, width=5, height=1)
        self.txt_interval.pack(side = "left", padx = (20, 0))
        
        # Select interval unit
        self.cb_interval = ttk.Combobox(fr_exe, width=5, height=15, values=["sec", "min", "hour", "day", "week"], state="readonly")
        self.cb_interval.pack(side = "left", padx = (20, 0))

        # Set interval
        btn_set_interval = Button(fr_exe, command=self.setInterval, width=10, height=1, text="Set", background = "#AAAAAA")
        btn_set_interval.bind("<Enter>", lambda event : self._on_enter(self, btn_set_interval))
        btn_set_interval.bind("<Leave>", lambda event : self._on_leave(self, btn_set_interval))
        btn_set_interval.pack(side = "left", padx = (20, 0))

        # Stop monitoring
        btn_stop = Button(fr_exe, command=self.stop, width=10, height=1, text="STOP", background = "#AAAAAA")
        btn_stop.bind("<Enter>", lambda event : self._on_enter(self, btn_stop))
        btn_stop.bind("<Leave>", lambda event : self._on_leave(self, btn_stop))
        # btn_stop.grid(row = 0, column = 1, sticky = "e")
        btn_stop.pack(side = "right", anchor = "e", padx = 20)

        # Run monitoring
        btn_run = Button(fr_exe, command=self.rerun, width=10, height=1, text="RUN", background = "#AAAAAA")
        btn_run.bind("<Enter>", lambda event : self._on_enter(self, btn_run))
        btn_run.bind("<Leave>", lambda event : self._on_leave(self, btn_run))
        # btn_run.grid(row = 0, column = 0, sticky = "e")
        btn_run.pack(side = "right", anchor = "e")

        # Clear UI
        self.clearUi()
        self.reloadUi()

        self.logger.info("_init_ui finished.")


    ############### Common ###############
    def _on_enter(self, event, btn : Button):
        btn["background"] = "#CCCCCC"
        
    def _on_leave(self, event, btn : Button):
        btn["background"] = "#AAAAAA"

    def updateComboBox(self, drive_list : list):
        self.cb_drive.delete(0, END)
        self.cb_drive["values"] = drive_list

        if drive_list:
            self.cb_drive.current(0)
            drive = drive_list[0]
            self.showMaxSpaceRate(drive)

    def updateListBox(self, list_dirs : list) -> None:
        for dir_path in list_dirs:
            self.list_dirs.insert("end", dir_path)

    def updateInterval(self, interval : dict) -> None:
        interval_keys = interval.keys()

        if "value" in interval_keys:
            self.txt_interval.delete(1.0 , END)
            self.txt_interval.insert(END, interval["value"])

        if "unit" in interval_keys:
            self.cb_interval.current(interval["unit"])

    def clearUi(self) -> None:
        self.cb_drive.delete(0, END)
        self.txt_max_space_rate.delete(1.0 , END)
        self.list_dirs.delete(0, END)
        self.chk_var_auto_run.set(False)
        self.txt_interval.delete(1.0, END)
        self.cb_interval.set("")

    def reloadUi(self) -> None:
        self.updateComboBox(self.fm.getDriveList())
        self.updateListBox(self.fm.getDirList())
        self.chk_var_auto_run.set(self.fm.isAutoRun())
        self.updateInterval(self.fm.getIntervalDict())

    def intervalTest(self):
        self.cb_interval.set("")
        
    def onClickCheckButton(self) -> None:
        self.fm.setAutoRun(bool(self.chk_var_auto_run.get()))


    ############### Config ###############
    def selectSavePath(self) -> None:
        dir_path = filedialog.askdirectory(title="Select directory to save config")
        
        if dir_path:
            self.txt_save_config_path.config(state="normal")
            self.txt_save_config_path.delete(1.0 , END)
            self.txt_save_config_path.insert(END, dir_path + "/cfg.json")
            self.txt_save_config_path.config(state="disabled")

    def loadConfig(self, config_path : str = "") -> bool:
        self.logger.info("loadConfig started.")

        if not config_path:
            self.logger.info("Load default config")
            config_path = self.initial_dir + "config.cfg"

        self.logger.info(f"Load config : {config_path}")

        if not osp.exists(config_path):
            self.logger.warning(f"Wrong config path")
            return False

        with open(config_path, "r") as f:
            config = json.load(f)

        config_keys = config.keys()

        if "dir_list" not in config_keys:
            config["dir_list"] = []
            
        if "drive_list" not in config_keys:
            config["drive_list"] = []
            
        if "max_space_rate" not in config_keys:
            config["max_space_rate"] = dict()
            
        if "auto_run" not in config_keys:
            config["auto_run"] = False
            
        if "interval" not in config_keys:
            config["interval"] = dict()
        else:
            interval_sec = self._getIntervalSec(config["interval"])
            if interval_sec > 0:
                self.worker.setInterval(interval_sec)

        self.fm.setConfig(config)

        self.logger.info("loadConfig finished.")

        return True

    def importConfig(self) -> bool:
        file_path = filedialog.askopenfilename(initialdir = self.initial_dir, title = "Import config file",
                                               filetypes = (("config files", "*.cfg"), ("all files", "*.*")),
                                               defaultextension = ".*")

        if not file_path:
            self.logger.warning("Config file not selected")
            return False
        
        loaded = self.loadConfig(file_path)
    
        self.clearUi()
        self.reloadUi()

        return loaded
    
    def exportConfig(self) -> bool:
        file_path = filedialog.asksaveasfilename(initialdir = self.initial_dir, title = "Export config file",
                                                 filetypes = (("config files", "*.cfg"), ("all files", "*.*")),
                                                 defaultextension = ".*")
        
        if not file_path:
            self.logger.warning("Config save path not entered")
            return False
        
        config = self.fm.getConfig()

        with open(file_path, "w") as f:
            json.dump(config, f)
        
        return True


    ############### Drive ###############
    def showMaxSpaceRate(self, event) -> None:
        # drive = from drive combobox
        # rate = from rate text edit
        # return self.fm.setMaxSpaceRate(drive, rate)

        drive = self.cb_drive.get()

        if not drive:
            self.logger.warning("Drive not selected")
            return
        
        if drive not in self.fm.getDriveList():
            self.logger.warning(f"{drive} not in drive list")
            return
        
        self.txt_max_space_rate.delete(1.0 , END)
        self.txt_max_space_rate.insert(END, self.fm.getMaxSpaceRate(drive) * 100)

        return
    
    def setMaxSpaceRate(self) -> bool:
        drive = self.cb_drive.get()
        max_space_rate = self.txt_max_space_rate.get(1.0 , END)

        if not isNumber(max_space_rate):
            # message box : "Not valid number"
            msg.showerror("Error", "Max space rate is not number.\nEnter number between 0 and 100.")
            self.logger.warning("Max space rate is not number. Enter number between 0 and 100.")
            return False
        
        f_max_space_rate = float(max_space_rate)

        if f_max_space_rate < 0 or f_max_space_rate > 100:
            msg.showerror("Error", "Max space rate is not in valid range.\nEnter number between 0 and 100.")
            self.logger.warning("Max space rate is not in valid range. Enter number between 0 and 100.")
            return False


        # message box : "Do you want to set max space rate to 'f_max_space_rate'?"
        result = msg.askokcancel("Set max space", f"Do you want to set max sapce rate to \n{f_max_space_rate} ?")
        
        if not result:
            return False

        return self.fm.setMaxSpaceRate(drive, f_max_space_rate * 0.01)


    ############### Directories ###############
    def addDir(self) -> None:
        dir_path = filedialog.askdirectory(title = "Select directory to monitor")

        if not dir_path:
            self.logger.warning("directory not selected")
            return

        if not self.fm.addDir(dir_path):
            self.logger.warning(f"Failed to add directory : {dir_path}")
            return
        
        self.list_dirs.insert("end", dir_path)

        self.logger.info(f"{dir_path} added.")

        self.updateComboBox(self.fm.getDriveList())
        # self.showMaxSpaceRate(dir_path)

    def removeDir(self) -> None:
        selected = self.list_dirs.curselection()

        self.logger.info(f"{selected} selected")

        if not selected:
            # message box : "Select directory to remove"
            msg.showerror("Error", "Select directory to remove.")
            self.logger.warning("Directory to remove not selected")
            return

        dir_path = self.list_dirs.get(selected)
        
        # message box : "Do you want to remove 'directory_name'"?
        result = msg.askokcancel("Remove directory", f"Do you want to remove \n{dir_path} ?")

        if not result:
            return
        
        if not self.fm.removeDir(dir_path):
            self.logger.warning(f"Failed to remove directory : {dir_path}")
            return
        
        self.list_dirs.delete(selected, selected)

        self.logger.info(f"{dir_path} removed.")
        

    ############### Execute ###############
    def setInterval(self) -> None:
        interval_value = self.txt_interval.get(1.0 , END).strip()
        interval_unit = self.cb_interval.current()
        interval_unit_str = self.cb_interval["values"][interval_unit]
        print(interval_unit_str)
        
        result = msg.askokcancel("Set interval", f"Do you want to set interval to {interval_value} {interval_unit_str} ?")
        
        if not result:
            return False

        if not isNumber(interval_value):
            self.logger.warning(f"Input interval({interval_value}) is not number")
            return
        
        interval = {"value" : int(interval_value), "unit" : interval_unit}
        
        interval_sec = self._getIntervalSec(interval)

        if interval_sec < 0:
            return
        
        self.logger.info(f"Set interval to {interval_value} {interval_unit_str}")

        self.fm.setIntervalDict(interval)
        self.worker.setInterval(interval_sec)
    
    def _getIntervalSec(self, interval : dict) -> int:
        if "value" not in interval:
            self.logger.warning("value is not in interval dict")
            return

        if "unit" not in interval:
            self.logger.warning("unit is not in interval dict")
            return

        interval_sec = interval["value"]
        interval_unit = interval["unit"]
        mult = 1

        if interval_unit == 0:      # sec
            mult = 1
        elif interval_unit == 1:    # min
            mult = 60
        elif interval_unit == 2:    # hour
            mult = 60 * 60
        elif interval_unit == 3:    # day
            mult = 60 * 60 * 24
        elif interval_unit == 4:    # week
            mult = 60 * 60 * 24 * 7
        else:
            self.logger.warning(f"interval unit({interval_unit}) is not in range")
            return -1
        
        interval_sec *= mult

        return interval_sec

    def run(self) -> None:
        if self.worker is None:
            self.logger.warning("Thread does not exist.")
            return

        if self.fm is None:
            self.logger.warning("File Manager is not defined.")
            return

        if self.fm.isAutoRun():
            self.worker.rerun()
        
        self.worker.start()

    def rerun(self) -> None:
        if self.worker is None:
            self.logger.warning("Thread does not exist.")
            return
        
        if self.worker.isRunning():
            msg.showwarning("Warning", "Monitoring is already runnning.")
            self.logger.info("Monitoring is already runnning.")
            return

        self.worker.rerun()
        
        # message box : "Run monitoring"
        msg.showinfo("Info", "Run monitoring.")
        self.logger.info("Run monitoring.")
        pass
        

    def stop(self) -> None:
        if self.worker is None:
            self.logger.warning("Thread does not exist.")
            return

        if not self.worker.isRunning():
            msg.showwarning("Warning", "Monitoring is not running.")
            self.logger.info("Monitoring is not running.")
            return
        
        # message box : "Do you want to stop monitoring"
        result = msg.askokcancel("Stop monitoring", "Do you want to stop monitoring?")
        
        if not result:
            return
        
        self.logger.info("Stop monitoring.")

        self.worker.stop()


if __name__ == "__main__":
    app = App()
    app.mainloop()