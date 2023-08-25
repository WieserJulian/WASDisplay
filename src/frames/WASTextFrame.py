import logging
import re

from customtkinter import CTkFrame, CTkLabel, CTkFont

from utils.Emergency import Emergency
from utils.util_functions import reformat_austrian_phone_number

from utils.config import Config


class WASTextFrame(CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        # self.grid_columnconfigure(0, weight=1)
        self.config = Config()
        self.offset_state = -1
        self.allEmergency = []
        self.allEmergencyIDs = {}

    def changeWAS(self, active_operations: dict):
        for emergency_id in active_operations.keys():
            emergency = active_operations[emergency_id]
            if emergency.status == 'Alarmiert' and emergency_id not in self.allEmergencyIDs:
                self.addEmergency(emergency)
            elif len(self.allEmergencyIDs - active_operations.keys()) != 0:
                self.deleteEmergency(list(self.allEmergencyIDs.keys() - active_operations.keys()))
            elif emergency.status == 'Ausgerückt':
                self.changeState(emergency)
        if len(active_operations.keys()) == 0:
            self.deleteEmergency(list(self.allEmergencyIDs.keys()))

    def addEmergency(self, emergency: Emergency):
        emergency_frame = CTkFrame(self)
        emergency_frame.grid_columnconfigure(2, weight=1)
        emergency_frame.grid_rowconfigure(5, weight=1)
        font = CTkFont(size=32, weight="bold")
        font2 = CTkFont(size=14)

        nameAndLevel = CTkLabel(emergency_frame, font=font,
                                text="{} Alst. {}".format(emergency.operationName, emergency.level))
        nameAndLevel.grid(row=0, column=0, padx=20, pady=10)

        location = CTkLabel(emergency_frame, font=font, text="Ort: {}".format(emergency.location))
        location.grid(row=1, column=0, padx=20, pady=10)

        caller_name = CTkLabel(emergency_frame, font=font, text="Anrufer: {}".format(emergency.name))
        caller_name.grid(row=2, column=0, padx=20, pady=10)

        if emergency.caller is not None:
            cal = reformat_austrian_phone_number(emergency.caller)
            caller = CTkLabel(emergency_frame, font=font, text="Telefonnummer: {}".format(cal))
            caller.grid(row=3, column=0, padx=20, pady=10)

        origin = CTkLabel(emergency_frame, font=font, text="Von {}".format(emergency.origin))
        origin.grid(row=4, column=0, padx=20, pady=10)

        IDandDate = CTkLabel(emergency_frame, font=font2, text="ID: {} {}".format(emergency.id, emergency.receiveTad))
        IDandDate.grid(row=5, column=0, padx=20, pady=5)

        status_frame = CTkFrame(emergency_frame, fg_color="red")
        status_frame.grid(row=0, rowspan=6, column=1, padx=(0, 10), pady=0, sticky="nes")

        emergency_frame.pack(anchor="center", pady=5, padx=1, fill="x")
        self.allEmergency.append(emergency_frame)
        self.allEmergencyIDs[emergency.id] = status_frame

    def changeState(self, emergency: Emergency):
        frame: CTkFrame = self.allEmergencyIDs.get(emergency.id)
        frame.configure(fg_color="green")

    def deleteEmergency(self, to_remove: list):
        for rem in to_remove:
            frame: CTkFrame = self.allEmergency[list(self.allEmergencyIDs.keys()).index(rem)]
            frame.destroy()
            self.allEmergency.remove(frame)
            self.allEmergencyIDs.pop(rem)
