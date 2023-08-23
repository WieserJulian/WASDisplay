import enum

import customtkinter


class MODULES(enum.Enum):
    PRINTER = 0
    PRINTER_SETTING = 1


class Settings(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Einstellungen")
        self.after(200, lambda: self.iconbitmap("assets/Feuerwehr.ico"))
        self.geometry("800x500")
        self.resizable(width=False, height=False)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.tab_frame = customtkinter.CTkTabview(self)
        title_font = customtkinter.CTkFont(size=20)
        # Allgemein Tab
        self.tab_frame.add("Allgemein")
        # self.tab_frame.set("Allgemein")
        self.tab_frame.tab("Allgemein").grid_columnconfigure(0, weight=1)
        self.title_alg = customtkinter.CTkLabel(self.tab_frame.tab("Allgemein"), text="Allgemeine Einstellungen",
                                                font=title_font)
        self.title_alg.grid(row=0, column=0, columnspan=1, pady=5, padx=5, sticky=customtkinter.NSEW)

        # Functions Tab
        self.tab_frame.add("Funktionen")
        self.tab_frame.set("Funktionen")
        self.tab_frame.tab("Funktionen").grid_columnconfigure(0, weight=1)
        self.title_func = customtkinter.CTkLabel(self.tab_frame.tab("Funktionen"), text="Steuerung aller Funktionen",
                                                 font=title_font)
        self.printer_enable_frame = self.add_settings_frame(self.tab_frame.tab("Funktionen"), "Drucker Module",
                                                            customtkinter.CTkSwitch, MODULES.PRINTER, text="")
        self.printer_enable_frame.grid(row=1, column=0, padx=5, pady=5, sticky=customtkinter.NSEW)
        self.printer_piece_frame = self.add_settings_frame(self.tab_frame.tab("Funktionen"), "Anzahl der Ausdrucke: ",
                                                           customtkinter.CTkEntry, MODULES.PRINTER_SETTING,
                                                           placeholder_text="1")
        self.tab_frame.grid(row=0, column=0, padx=20, pady=20, sticky=customtkinter.NSEW)

    def add_settings_frame(self, master, title: str, cls, module: MODULES, **kwargs) -> customtkinter.CTkFrame:
        frame = customtkinter.CTkFrame(master, bg_color='transparent')
        tl = customtkinter.CTkLabel(frame, text=title, font=customtkinter.CTkFont(size=20))
        tl.grid(row=1, column=0, pady=2, padx=5, sticky=customtkinter.E)
        if cls is not customtkinter.CTkEntry:
            setting = cls(frame, command=lambda: self.enable(module, setting), **kwargs)
            setting.grid(row=1, column=1, pady=2, padx=5, sticky=customtkinter.W)
        else:
            setting = cls(frame, **kwargs)
            setting.grid(row=1, column=1, pady=2, padx=5, sticky=customtkinter.W)
        return frame

    def enable(self, module: MODULES, setting):
        match module:
            case MODULES.PRINTER:
                if setting.get() == 1:
                    self.printer_piece_frame.grid(row=2, column=0, padx=5, pady=5, sticky=customtkinter.NSEW)
                else:
                    self.printer_piece_frame.grid_forget()
            case MODULES.PRINTER_SETTING:
                print(setting.get())
