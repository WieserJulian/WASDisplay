#  ******************************************************
#  * Copyright (C) 2023 Julian Wieser
#  * julian.wieser@i-wieser.com
#  *
#  * This project can not be copied and/or distributed without the express
#  * permission of Julian Wieser
#  *******************************************************
import threading
from concurrent import futures

import customtkinter

from src.WASCommunication import WASCommunication
from src.WASTextFrame import WASTextFrame

DEBUG = True

thread_pool_executor = futures.ThreadPoolExecutor(max_workers=1)


class Display(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("WAS Erweiterungs Oberfläche")
        # self.overrideredirect(True)
        self.geometry("{0}x{1}+0+0".format(self.winfo_screenwidth(), self.winfo_screenheight()))
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(2, weight=1)
        # add widgets to app
        self.wasCommunication = WASCommunication(self, DEBUG)
        self.wasFrame = WASTextFrame(self)
        self.wasFrame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        # Start Thread for WAS Communication

        self.bind("<<WASCommunication>>", self.changeWAS)
        self.communicate_WAS()

    def button_click(self):
        print("button click")

    def communicate_WAS(self):
        self.wasCommunication.readSocket()
        self.after(2000, self.communicate_WAS)

    def changeWAS(self, event):
        self.wasFrame.changeWAS(self.wasCommunication.active_operations)
