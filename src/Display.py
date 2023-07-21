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

DEBUG = True

thread_pool_executor = futures.ThreadPoolExecutor(max_workers=1)


class Display(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("WAS Erweiterungs Oberfläche")
        # self.overrideredirect(True)
        self.geometry("{0}x{1}+0+0".format(self.winfo_screenwidth(), self.winfo_screenheight()))
        # add widgets to app
        self.wasCommunication = WASCommunication(self, DEBUG)
        self.button = customtkinter.CTkButton(self, command=self.button_click)
        self.button.grid(row=0, column=0, padx=20, pady=10)
        self.bind("<<WASCommunication>>", self.change_WAS)
        # Start Thread for WAS Communication
        self.communicate_WAS()

    # add methods to app
    def button_click(self):
        print("button click")

    def communicate_WAS(self):
        threading.Thread(self.wasCommunication.readSocket()).start()
        self.after(5000, self.communicate_WAS())

    def change_WAS(self, event):
        print(self.wasCommunication.active_operations)