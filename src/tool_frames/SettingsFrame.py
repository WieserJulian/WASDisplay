import enum
import sys
import os
import tkinter.messagebox

import customtkinter

from utils.config import Config


class MODULES(enum.Enum):
    PRINTER = 0
    PRINTER_SETTING = 1
    APPEARANCE = 2
    LOCATION = 3,
    DEBUG = 4
    REQUEST_TIME = 5


class Settings(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Einstellungen")
        self.after(200, lambda: self.iconbitmap(self.config.icon_path))
        self.geometry("800x500")
        self.resizable(width=False, height=False)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.config = Config()
        self.tab_frame = customtkinter.CTkTabview(self)
        self.int_validator = (self.register(self.validate_int), '%P')
        self.address_validator = (self.register(self.validate_adr), '%P')
        title_font = customtkinter.CTkFont(size=20)
        self.debug_var = self.config.settings.default.debug
        # Allgemein Tab
        self.tab_frame.add("Allgemein")
        self.tab_frame.set("Allgemein")
        self.tab_frame.tab("Allgemein").grid_columnconfigure(0, weight=1)
        self.location_frame = self.add_settings_frame(self.tab_frame.tab("Allgemein"), "Feuerwehr Addresse: ",
                                                      customtkinter.CTkEntry, MODULES.LOCATION,
                                                      placeholder_text="Petzoldstraße 43, Linz, Austria",
                                                      text=self.config.settings.default.place_depo,
                                                      validate='focusout', validatecommand=self.address_validator)
        self.location_frame.grid(row=0, column=0, padx=5, pady=5, sticky=customtkinter.NSEW)

        self.system_modus = self.add_settings_frame(self.tab_frame.tab("Allgemein"), "Systemmodus",
                                                    customtkinter.CTkSwitch, MODULES.APPEARANCE,
                                                    self.config.settings.default.appearance, onvalue='light',
                                                    offvalue='dark', text="")
        self.system_modus.grid(row=1, column=0, padx=5, pady=5, sticky=customtkinter.NSEW)

        self.debug_mode = self.add_settings_frame(self.tab_frame.tab("Allgemein"), "TestModus",
                                                  customtkinter.CTkSwitch, MODULES.DEBUG,
                                                  self.config.settings.default.debug, text="")
        self.debug_mode.grid(row=2, column=0, padx=5, pady=5, sticky=customtkinter.NSEW)

        # self.request_time_frame = self.add_settings_frame(self.tab_frame.tab("Allgemein"), "Abfrage Zeit (sekunden) ",
        #                                               customtkinter.CTkEntry, MODULES.REQUEST_TIME,
        #                                               text=self.config.settings.default.request_time,
        #                                               validate='key', validatecommand=self.int_validator)
        # self.request_time_frame.grid(row=3, column=0, padx=5, pady=5, sticky=customtkinter.NSEW)
        # Functions Tab
        self.tab_frame.add("Funktionen")
        # self.tab_frame.set("Funktionen")
        self.tab_frame.tab("Funktionen").grid_columnconfigure(0, weight=1)
        self.title_func = customtkinter.CTkLabel(self.tab_frame.tab("Funktionen"), text="Steuerung aller Funktionen",
                                                 font=title_font)
        self.printer_frame = customtkinter.CTkFrame(self.tab_frame.tab("Funktionen"))
        self.printer_frame.grid_columnconfigure(0, weight=1)
        self.printer_enable_frame = self.add_settings_frame(self.printer_frame, "Drucker Module",
                                                            customtkinter.CTkSwitch, MODULES.PRINTER,
                                                            self.config.settings.settings.printer.active, text="")
        self.printer_enable_frame.grid(row=0, column=0, padx=5, pady=5, sticky=customtkinter.NSEW)

        self.printer_piece_frame = self.add_settings_frame(self.printer_frame, "Anzahl der Ausdrucke: ",
                                                           customtkinter.CTkEntry, MODULES.PRINTER_SETTING,
                                                           text=self.config.settings.settings.printer.amount,
                                                           validate='key', validatecommand=self.int_validator)
        if self.config.settings.settings.printer.active:
            self.printer_piece_frame.grid(row=1, column=0, padx=(30, 5), pady=5, sticky=customtkinter.NSEW)

        self.printer_frame.grid(row=0, column=0, padx=5, pady=5, sticky=customtkinter.NSEW)
        self.tab_frame.grid(row=0, column=0, padx=20, pady=20, sticky=customtkinter.NSEW)
        self.save = customtkinter.CTkButton(self, text="Speichern", command=self.save_settings)
        self.save.grid(row=1, column=0, padx=5, pady=10, sticky=customtkinter.E)

    def save_settings(self):
        self.config.settings.settings.printer.amount = int(
            self.get_entry(self.printer_piece_frame, self.config.settings.settings.printer.amount))
        self.config.settings.default.place_depo = self.get_entry(self.location_frame,
                                                                 self.config.settings.default.place_depo)
        # self.config.settings.default.request_time = int(self.get_entry(self.request_time_frame,
        #                                                            self.config.settings.default.request_time))
        if self.debug_var != self.config.settings.default.debug:
            res = tkinter.messagebox.askokcancel("Restart", "Es wird ein Neustart benötigt!")
            if res:
                self.config.settings.default.debug = bool(self.debug_var)
                self.config.write()
                self.destroy()
                self.master.destroy()
                return
            else:
                self.destroy()
        else:
            self.config.write()
            self.destroy()

    def get_entry(self, frame, default_value):
        re = frame.children.get(list(frame.children.keys())[-1]).get()
        return re if re != "" else default_value

    def add_settings_frame(self, master, title: str, cls, module: MODULES, set_active=False, text="",
                           **kwargs) -> customtkinter.CTkFrame:
        frame = customtkinter.CTkFrame(master, bg_color='transparent')
        frame.grid_columnconfigure(1, weight=1)
        tl = customtkinter.CTkLabel(frame, text=title, font=customtkinter.CTkFont(size=20))
        tl.grid(row=1, column=0, pady=2, padx=5, sticky=customtkinter.E)
        if cls is not customtkinter.CTkEntry:
            setting = cls(frame, text="", command=lambda: self.enable(module, setting), **kwargs)
            if set_active:
                setting.select()
            setting.grid(row=1, column=1, pady=2, padx=5, sticky=customtkinter.W)
        else:
            setting = cls(frame, **kwargs)
            if text != "":
                setting.insert(0, text)
            setting.grid(row=1, column=1, pady=2, padx=5, sticky=customtkinter.EW)
        return frame

    def enable(self, module: MODULES, setting):
        match module:
            case MODULES.PRINTER:
                if setting.get() == 1:
                    self.config.settings.settings.printer.active = True
                    self.printer_piece_frame.grid(row=2, column=0, padx=(30, 5), pady=5, sticky=customtkinter.NSEW)
                else:
                    self.config.settings.settings.printer.active = False
                    self.printer_piece_frame.grid_forget()
            case MODULES.APPEARANCE:
                customtkinter.set_appearance_mode(setting.get())
            case MODULES.DEBUG:
                self.debug_var = setting.get()

    def validate_int(self, key):
        if key == "":
            return True
        try:
            int(key)
            return True
        except ValueError:
            return False

    def validate_adr(self, key):
        if key == "":
            return True
        try:
            # TODO needs validation
            from osmnx import geocoder
            # geocoder.geocode(query=key+", Austria")
            print(True, key + ", Austria")
            return True
        except Exception as e:
            print(False, e, key + ", Austria")
            return False
