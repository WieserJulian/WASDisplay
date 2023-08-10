import uuid
import socket

import customtkinter

from src.config import Config


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("600x500")
        self.title("Test Sender")
        self.command = ""

        self.status = customtkinter.CTkLabel(self, text="UnConnected")
        self.status.pack()

        self.connect = customtkinter.CTkButton(self, text="Connect", command=self.connect_fc)
        self.connect.pack()

        self.operation_id = customtkinter.CTkLabel(self, text="E"+uuid.uuid4().__str__())
        self.operation_id.pack()
        self.operation_name = customtkinter.CTkEntry(self, placeholder_text="Test Alarm")
        self.operation_name.pack()
        self.operation_address = customtkinter.CTkEntry(self, placeholder_text="Addresse")
        self.operation_address.pack()
        self.operation_state = customtkinter.CTkOptionMenu(self, values=['Alarmiert', 'Ausgerückt', 'Fertig'])
        self.operation_state.set('Alamiert')
        self.operation_state.pack()



        # add widgets to app
        self.send = customtkinter.CTkButton(self,text="Send", command=self.send)
        self.send.pack()

    def connect_fc(self):
        self.status.configure(text="Connected")
    # add methods to app
    def send(self):
        self.build_command()
        x = self.command.encode('utf-8')
        s = socket.socket()
        s.connect(('localhost', 8080))
        s.send(x)
        s.close()

    def build_command(self):
        if (self.operation_state.get() == 'Fertig'):
            self.command = ""
        else:
            self.command = f"""<pdu>
                        <order-list count="1">
                            <order index="1">
                                    <key>0x016d48b8</key>
                                    <origin tid="0000000">LFKOO</origin>
                                    <receive-tad>2019-11-06 17:58:49</receive-tad>
                                    <operation-id>{self.operation_id.cget("text")}</operation-id>
                                    <level>1</level>
                                    <name>TEST</name>
                                    <operation-name>{self.operation_name.get()}</operation-name>
                                    <caller></caller>
                                    <location>{self.operation_address.get()}</location>
                                    <info>TEST</info>
                                    <program>Stiller Alarm oHT</program>
                                    <status>{self.operation_state.get()}</status>
                                    <watch-out-tad></watch-out-tad>
                                    <finished-tad></finished-tad>
                                    <destination-list count="1">
                                    <destination index="1" id="34101">ALKOVEN</destination>
                                    </destination-list>
                                    <paging-destination-list count="0">
                                    </paging-destination-list>
                            </order>
                        </order-list>
                </pdu>"""



if __name__ == '__main__':
    app = App()
    app.mainloop()