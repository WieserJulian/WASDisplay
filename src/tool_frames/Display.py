#  ******************************************************
#  * Copyright (C) 2023 Julian Wieser
#  * julian.wieser@i-wieser.com
#  *
#  * This project can not be copied and/or distributed without the express
#  * permission of Julian Wieser
#  *******************************************************

import customtkinter

from tool_frames.MenuBar import MenuBar
from utils.WASCommunication import WASCommunication
from frames.WASTextFrame import WASTextFrame
from tool_frames.SnackBarFrame import SnackBar

DEBUG = True


class Display(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.__load_config()

        # add widgets to app
        self.wasCommunication = WASCommunication(self, DEBUG)
        self.wasFrame = WASTextFrame(self, width=int(self.winfo_screenwidth() * (1 / 3)))
        self.wasFrame.grid(row=0, column=0, padx=20, pady=(20, 0), sticky="nsew")

        self.map_frame = customtkinter.CTkFrame(self, bg_color='transparent',
                                                width=int(self.winfo_screenwidth() * (2 / 2)))
        self.map_frame.grid(row=0, column=1, padx=20, pady=(20, 0), sticky="nsew")
        self.snackbar = SnackBar(self, height=40)
        self.snackbar.grid(row=1, column=0, columnspan=2, padx=20, pady=5, sticky=customtkinter.NSEW)
        # Start Thread for WAS Communication

        self.bind("<<WASCommunication>>", self.changeWAS)
        self.bind("<<StatusChanged>>", self.snackbar.change_status)
        self.configure(menu=MenuBar(self))
        self.communicate_WAS()

    def __load_config(self):
        global DEBUG
        self.title("WAS Erweiterungs Oberfläche")
        self.iconbitmap("assets/Feuerwehr.ico")
        customtkinter.set_appearance_mode("light")
        customtkinter.set_widget_scaling(1)
        self.geometry("{0}x{1}+0+0".format(self.winfo_screenwidth(), self.winfo_screenheight()))
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        if not DEBUG:
            self.overrideredirect(True)
        else:
            self.geometry("{0}x{1}+0+0".format(self.winfo_screenwidth(), self.winfo_screenheight() - 100))

    def on_closing(self):
        self.wasCommunication.socket.close()
        self.destroy()

    def communicate_WAS(self):
        self.wasCommunication.readSocket()
        self.after(2000, self.communicate_WAS)

    def changeWAS(self, event):
        self.wasFrame.changeWAS(self.wasCommunication.active_operations)
