import customtkinter


class Settings(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x300")
        self.title = "Einstellungen"
        self.label = customtkinter.CTkLabel(self, text="Settings")
        self.label.pack(padx=20, pady=20)
