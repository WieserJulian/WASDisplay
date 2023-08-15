import uuid
import socket

import customtkinter

from src.config import Config


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1000x500")
        self.title("Test Sender")
        self.command = "<pdu></pdu>"
        self.all_emergency = {}
        self.all_em_frame = []

        self.status = customtkinter.CTkLabel(self, text="UnConnected", font=customtkinter.CTkFont(size=24),
                                             text_color='red')
        self.status.pack()

        self.test_emergency_frame = customtkinter.CTkFrame(self, height=20)
        self.test_emergency_frame.pack()
        self.add_button = customtkinter.CTkButton(self, text="Add Emergency", command=self.add_em)
        self.add_button.pack()

        # add widgets to app
        self.reconnect()
        self.after(1000, self.send_fc)

    def add_em(self):
        frame = customtkinter.CTkFrame(self.test_emergency_frame)
        operation_id = customtkinter.CTkLabel(frame, text="E" + uuid.uuid4().__str__(),
                                              font=customtkinter.CTkFont(size=10))
        operation_id.grid(row=0, column=0, padx=5)
        operation_name = customtkinter.CTkEntry(frame, placeholder_text="Test Alarm")
        operation_name.grid(row=0, column=1, padx=5)
        operation_address = customtkinter.CTkEntry(frame, placeholder_text="Addresse")
        operation_address.grid(row=0, column=2, padx=5)
        operation_state = customtkinter.CTkOptionMenu(frame, values=['None', 'Alarmiert', 'Ausgerückt', 'Fertig'])
        operation_state.set('None')
        operation_state.grid(row=0, column=3, padx=5)
        send = customtkinter.CTkButton(frame, text="Rebuild", command=lambda: self.rebuild_em(operation_id.cget('text'),
                                                                                              operation_name.get(),
                                                                                              operation_address.get(),
                                                                                              operation_state.get()))
        send.grid(row=0, column=4, padx=5)
        destroy = customtkinter.CTkButton(frame, text="Delete", command=lambda: self.delete_em(frame, operation_id.cget('text')))
        destroy.grid(row=0, column=5, padx=5)
        frame.grid(row=len(self.all_em_frame), pady=5)
        self.all_em_frame.append(frame)

    def delete_em(self, frame, id):
        self.all_emergency.pop(id)
        frame.destroy()
        self.build_command()

    def rebuild_em(self, id, name, address, state):
        emergency = [name, address, state]
        match state:
            case 'None':
                return
            case 'Alarmiert':
                self.all_emergency[id] = emergency
            case 'Ausgerückt':
                self.all_emergency[id] = emergency
            case 'Fertig':
                self.all_emergency.pop(id)
        self.build_command()

    # add methods to app
    def send_fc(self):
        x = self.command.encode('iso-8859-15')
        try:
            self.socket.send(x)
            print(x)
        except (ConnectionRefusedError, OSError):
            self.reconnect()
        self.after(2000, self.send_fc)

    def reconnect(self):
        print("[!] Try reconnect")
        try:
            host = "localhost"
            port = 8080
            self.socket = socket.socket()
            self.socket.connect((host, port))
            self.status.configure(text="Connected", text_color='green')
        except:
            self.status.configure(text="NOT Connected", text_color='red')
            self.after(1000, self.reconnect)

    def build_command(self):
        if len(self.all_emergency.keys()) <= 0:
            self.command = "<pdu></pdu>"
        else:
            self.command = f"""<pdu><order-list count="{len(self.all_emergency.keys())}" """
            for index, em_id in enumerate(self.all_emergency.keys()):
                em = self.all_emergency[em_id]
                self.command += f""">
                                <order index="{index}">
                                        <key>0x016d48b8</key>
                                        <origin tid="0000000">LFKOO</origin>
                                        <receive-tad>2019-11-06 17:58:49</receive-tad>
                                        <operation-id>{em_id}</operation-id><level>1</level>
                                        <name>TEST</name>
                                        <operation-name>{em[0]}</operation-name>
                                        <caller></caller>
                                        <location>{em[1]}</location>
                                        <info>TEST</info>
                                        <program>Stiller Alarm oHT</program>
                                        <status>{em[2]}</status>
                                        <watch-out-tad></watch-out-tad>
                                        <finished-tad></finished-tad>
                                        <destination-list count="1">
                                        <destination index="1" id="34101">ALKOVEN</destination>
                                        </destination-list>
                                        <paging-destination-list count="0">
                                        </paging-destination-list>
                                </order> 
                    """
            self.command += "</order-list></pdu>"


if __name__ == '__main__':
    app = App()
    app.mainloop()
