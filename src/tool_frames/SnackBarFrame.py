import tkinter

import customtkinter
from customtkinter import ThemeManager, AppearanceModeTracker


class SnackBar(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.grid_columnconfigure(1, weight=1)
        self.height = kwargs['height']
        self.circle_canvas = customtkinter.CTkCanvas(self, height=self.height, width=self.height,
                                                     bg=ThemeManager.theme["CTkFrame"]["fg_color"][AppearanceModeTracker.get_mode()])
        self.circle_canvas.grid(row=0, column=0, padx=(5, 10), pady=1, sticky=customtkinter.W)
        self.circle_canvas.create_aa_circle(int(self.height / 2) + 2, int(self.height / 2) + 2, int(self.height / 2), fill="red", tags="circle")

        self.status = customtkinter.CTkLabel(self, text="Nicht verbunden", font=customtkinter.CTkFont(size=14))
        self.status.grid(row=0, column=1, padx=5, pady=1, sticky=customtkinter.W)

    def change_status(self, event):
        if event.x == 1:
            self.status.configure(text="Verbunden")
            self.circle_canvas.delete("circle")
            self.circle_canvas.create_aa_circle(int(self.height / 2) + 2, int(self.height / 2) + 2,
                                                int(self.height / 2), fill="green", tags="circle")
        else:

            self.status.configure(text="Nicht verbunden")
            self.circle_canvas.delete("circle")
            self.circle_canvas.create_aa_circle(int(self.height / 2) + 2, int(self.height / 2) + 2,
                                                int(self.height / 2), fill="red", tags="circle")