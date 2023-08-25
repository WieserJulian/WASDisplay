import tkinter

import customtkinter
from PIL import Image
from customtkinter import ThemeManager, AppearanceModeTracker


class SnackBar(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.grid_columnconfigure(1, weight=1)
        self.height = kwargs['height'] - 10
        self.red_img = customtkinter.CTkImage(light_image=Image.open("assets/red_point.png"),
                                              dark_image=Image.open("assets/red_point.png"),
                                              size=(self.height, self.height))
        self.green_img = customtkinter.CTkImage(light_image=Image.open("assets/green_point.png"),
                                              dark_image=Image.open("assets/green_point.png"),
                                              size=(self.height, self.height))

        self.circle_img = customtkinter.CTkLabel(self, height=self.height, width=self.height, image=self.red_img, text="")
        self.circle_img.grid(row=0, column=0, padx=(5, 10), pady=1, sticky=customtkinter.W)

        self.status = customtkinter.CTkLabel(self, text="Nicht verbunden", font=customtkinter.CTkFont(size=14))
        self.status.grid(row=0, column=1, padx=5, pady=1, sticky=customtkinter.W)

    def change_status(self, event):
        if event.x == 1:
            self.status.configure(text="Verbunden")
            self.circle_img.configure(image=self.green_img)
        else:

            self.status.configure(text="Nicht verbunden")
            self.circle_img.configure(image=self.red_img)