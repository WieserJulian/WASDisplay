import os.path
import tkinter

import customtkinter
from PIL import Image
from customtkinter import ThemeManager, AppearanceModeTracker

from utils.config import Config


class SnackBar(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.grid_columnconfigure(1, weight=1)
        self.height = kwargs['height'] - 10
        self.green_img_path = os.path.join(Config().base_path, "assets/green_point.png")
        self.red_img_path = os.path.join(Config().base_path, "assets/red_point.png")
        self.red_img = customtkinter.CTkImage(light_image=Image.open(self.red_img_path),
                                              dark_image=Image.open(self.red_img_path),
                                              size=(self.height, self.height))
        self.green_img = customtkinter.CTkImage(light_image=Image.open(self.green_img_path),
                                              dark_image=Image.open(self.green_img_path),
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