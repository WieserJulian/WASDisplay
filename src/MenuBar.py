import customtkinter as ctk
import tkinter as tk

class MenuBar(tk.Menu):
    def __init__(self, master):
        super().__init__(master)

        # Adding File Menu and commands
        settings = tk.Menu(self, tearoff=0)
        self.add_command(label='Einstellungen', command=None)
        # settings.add_command(label='New File', command=None)