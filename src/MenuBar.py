import customtkinter as ctk
import tkinter as tk


class MenuBar(tk.Menu):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        # Adding File Menu and commands
        self.add_command(label='Einstellungen', command=self.open_settings)
        self.add_command(label='WASDisplay Beenden', command=self.close_application)
        # settings.add_command(label='New File', command=None)

    def close_application(self):
        self.master.event_generate("<<CLOSEAPP>>")


    def open_settings(self):
        pass
