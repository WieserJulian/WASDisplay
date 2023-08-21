#  ******************************************************
#  * Copyright (C) 2023 Julian Wieser
#  * julian.wieser@i-wieser.com
#  *
#  * This project can not be copied and/or distributed without the express
#  * permission of Julian Wieser
#  *******************************************************

import customtkinter

from MenuBar import MenuBar
from WASCommunication import WASCommunication
from WASTextFrame import WASTextFrame

DEBUG = True


class Display(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.__load_config()

        # add widgets to app
        self.wasCommunication = WASCommunication(self, DEBUG)
        self.wasFrame = WASTextFrame(self)
        self.wasFrame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.map_frame = customtkinter.CTkFrame(self, bg_color='transparent', width=int(self.winfo_screenwidth() / 2))
        self.map_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        # Start Thread for WAS Communication

        self.bind("<<WASCommunication>>", self.changeWAS)
        self.bind("<<CLOSEAPP>>", self.close_application)
        self.configure(menu=MenuBar(self))
        self.communicate_WAS()

    def __load_config(self):
        global DEBUG
        self.title("WAS Erweiterungs Oberfläche")
        customtkinter.set_appearance_mode("light")
        customtkinter.set_widget_scaling(1)
        self.geometry("{0}x{1}+0+0".format(self.winfo_screenwidth(), self.winfo_screenheight()))
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        if not DEBUG:
            self.overrideredirect(True)
        else:
            self.geometry("{0}x{1}+0+0".format(self.winfo_screenwidth(), self.winfo_screenheight() - 100))

    def close_application(self, x):
        self.destroy()
        self.wasCommunication.stop_reconnect()

    def communicate_WAS(self):
        self.wasCommunication.readSocket()
        self.after(2000, self.communicate_WAS)

    def changeWAS(self, event):
        self.wasFrame.changeWAS(self.wasCommunication.active_operations)
