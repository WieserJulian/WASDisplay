import re

from customtkinter import CTkFrame, CTkLabel, CTkFont

from Emergency import Emergency


class WASTextFrame(CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        # self.grid_columnconfigure(0, weight=1)
        self.offset_state = -1
        self.allEmergency = []
        self.allEmergencyIDs = {}

    def changeWAS(self, active_operations: dict):
        for emergency_id in active_operations.keys():
            emergency = active_operations[emergency_id]
            if emergency.status == 'Alarmiert' and emergency_id not in self.allEmergencyIDs:
                self.addEmergency(emergency)
            elif len(self.allEmergencyIDs - active_operations.keys()) != 0:
                self.deleteEmergency(self.allEmergencyIDs.keys() - active_operations.keys())
            elif emergency.status == 'Ausgerückt':
                self.changeState(emergency)
        if len(active_operations.keys()) == 0:
            self.deleteEmergency(self.allEmergencyIDs.keys())

    def addEmergency(self, emergency: Emergency):
        emergency_frame = CTkFrame(self)
        emergency_frame.grid_columnconfigure(2, weight=1)
        emergency_frame.grid_rowconfigure(5, weight=1)
        font = CTkFont(size=32, weight="bold")

        IDandDate = CTkLabel(emergency_frame, font=font, text="ID: {} {}".format(emergency.id, emergency.receiveTad))
        IDandDate.grid(row=0, column=0, padx=20, pady=5)

        origin = CTkLabel(emergency_frame, font=font, text="Von {}".format(emergency.origin))
        origin.grid(row=1, column=0, padx=20, pady=10)

        location = CTkLabel(emergency_frame, font=font, text=emergency.location)
        location.grid(row=2, column=0, padx=20, pady=10)

        nameAndLevel = CTkLabel(emergency_frame, font=font, text="{} Alst. {}".format(emergency.name, emergency.level))
        nameAndLevel.grid(row=3, column=0, padx=20, pady=10)

        if emergency.caller is not None:
            cal = self.reformat_austrian_phone_number(emergency.caller)
            caller = CTkLabel(emergency_frame, font=font, text="Anrufer: {}".format(cal))
            caller.grid(row=4, column=0, padx=20, pady=10)

        additionalInformation = CTkLabel(emergency_frame, font=font, text=emergency.operationName)
        additionalInformation.grid(row=5, column=0, padx=20, pady=10)

        status_frame = CTkFrame(emergency_frame, fg_color="red")
        status_frame.grid(row=0, rowspan=6, column=1, padx=(0, 10), pady=0, sticky="nes")

        emergency_frame.pack(anchor="center", pady=5, padx=1)
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

    @staticmethod
    def reformat_austrian_phone_number(phone_number):
        if phone_number is None:
            return phone_number
        # Remove all non-digit characters from the phone number
        digits_only = re.sub(r'\D', '', phone_number)

        # Check if the phone number is valid and has enough digits
        if not re.match(r'[0-9]*\/*(\+49)*(\+43)*(\+41)*[ ]*(\([0-9]{3,6}\))*([ ]*[0-9]|\/|\(|\)|\-|)*', digits_only):
            return phone_number

            # Reformat the phone number to the desired format
        formatted_number = f"+43 (0)6{digits_only[2:4]} {digits_only[4:7]} {digits_only[7:]}"

        return formatted_number
