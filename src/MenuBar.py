import customtkinter as ctk
import tkinter as tk

from Settings import Settings


class MenuBar(tk.Menu):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        # Adding File Menu and commands
        self.add_command(label='Einstellungen', command=self.open_settings)
        self.add_command(label='WASDisplay Beenden', command=self.close_application)


        self.settings_window = None

    def close_application(self):
        self.master.event_generate("<<CLOSEAPP>>")


    def open_settings(self):
        if self.settings_window is None or not self.settings_window.winfo_exists():
            self.settings_window = Settings(self)  # create window if its None or destroyed
        else:
            self.settings_window.focus()  # if window exists focus it
        pass
