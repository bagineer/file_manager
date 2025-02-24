import tkinter
from tkinter import *
from tkinter import ttk

from logger import Logger


class App(Tk):
    n_rows = 0

    def __init__(self):
        super().__init__()
        self.header = []
        self.widget_types = []
        
        self.title("Test")
        self.geometry("800x600")
        self.minsize(800, 600)

        fr_table = Frame(self, background = "red")
        fr_table.pack(fill = "both", ipadx = 15, ipady = 15)

        # # make two LabelFrames to fill horizontally
        # tab1.columnconfigure(0, weight=1)
        # # make two LabelFrames to evenly fill vertically
        # tab1.rowconfigure((0,1), weight=1)

        # header
        self.fr_header = Frame(fr_table, background = "blue")
        header = ["Directory", "Max Space(%)", "tmp1", "tmp2"]
        self.size_list = [15, 1, 1, 1]

        self.makeHeader(self.fr_header, header, self.size_list)
        self.setWidgetTypes(["Text", "Combobox", "Text", "Combobox"])

        self.fr_header.pack(fill = "x")

        fr_data = Frame(fr_table, background = "magenta")
        fr_data.pack(fill = "both")

        logger = Logger()
        logger.debug("asdf")

        self.insertRow(fr_data, 0, ["1", "2", "3", "4"])

        self.setColumnSize(self.fr_header, fr_data, self.size_list)
    # # develop
    # def defineStructure(self, header : list, widget_names : list):
    #     for widget_name in widget_names:
    #         widget = None
    #         if hasattr(tkinter, widget_name):
    #             widget = getattr(tkinter, widget_name)
    #         elif hasattr(ttk, widget_name):
    #             widget = getattr(ttk, widget_name)

    def makeHeader(self, fr_header : Frame, header : list, size_list : list) -> None:
        if len(header) != len(size_list):
            # wrong input
            return
        
        for i in range(len(header)):
            Label(fr_header, text = header[i], height = 1, relief="raised").grid(row = 0, column = i, sticky = "EW", ipadx = 15, ipady = 5)
            # fr_header.columnconfigure(i, weight = size_list[i])

        self.header = header

    def setColumnSize(self, fr_header : Frame, fr_data : Frame, size_list : list) -> None:
        if len(self.header) != len(size_list):
            # wrong input
            return

        for i in range(len(size_list)):
            # Label(fr_header, text = header[i], height = 1, relief="raised").grid(row = 0, column = i, sticky = "EW", ipadx = 15, ipady = 5)
            fr_header.columnconfigure(i, weight = size_list[i])
            fr_data.columnconfigure(i, weight = size_list[i])
        
    
    def setWidgetTypes(self, widget_types : list) -> None:
        if len(widget_types) != len(self.header):
            # wrong size
            return
        
        self.widget_types = widget_types

    def insertRow(self, fr_data : Frame, row_idx : int, data : list) -> None:
        if len(data) != len(self.header):
            # Wrong input data
            return
        
        for i in range(len(data)):
            widget = self.createWidget(self.widget_types[i], fr_data)
            
            if not widget:
                return

            widget.grid(row = row_idx, column = i, sticky = "EW", ipadx = 15, ipady = 5)
        
        

    def createWidget(self, widget_name : str, *args):
        if hasattr(tkinter, widget_name):
            print("widget 1", widget_name)
            return getattr(tkinter, widget_name)(*args)
        elif hasattr(ttk, widget_name):
            print("widget 2", widget_name)
            return getattr(ttk, widget_name)(*args)
        else:
            print("widget 3", widget_name)
            # wrong widget
            pass

        return None
    
    def deleteRow(self, table, row):
        pass



    def test(self):
        pass

if __name__ == "__main__":
    app = App()
    app.mainloop()