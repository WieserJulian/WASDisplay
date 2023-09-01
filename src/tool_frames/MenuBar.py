import customtkinter
from tool_frames.SettingsFrame import Settings


class MenuBar(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master, height=20)
        self.master = master
        # Adding File Menu and commands
        self.open_settings = customtkinter.CTkButton(self, text='Einstellungen', command=self.open_settings, fg_color="gray45")
        self.open_settings.grid(row=0, column=0, padx=5, sticky=customtkinter.W)
        self.settings_window = None

    def close_application(self):
        self.master.event_generate("<<CLOSEAPP>>")

    def open_settings(self):
        if self.settings_window is None or not self.settings_window.winfo_exists():
            self.settings_window = Settings(self.master)
            self.settings_window.focus_force()
        else:
            self.settings_window.focus_force()

