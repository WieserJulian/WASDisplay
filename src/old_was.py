import smtplib
import socket
import time
import xml.etree.ElementTree as ET
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

"""
Todos:
- send information about active operations to website
"""

HOST = '192.168.130.100'
PORT = 47000



def sendEmail(to_email, subject, message_text, message_html):
    SMTP_PORT = 587
    SMTP_SERVER = 'smtp.world4you.com'
    SMTP_SENDER_EMAIL = 'noreply@feuerwehr-alkoven.at'
    SMTP_PASSWORD = 'ndEb#5anti'
    debuglevel = 0
    smtp = smtplib.SMTP()
    smtp.set_debuglevel(debuglevel)
    smtp.connect(SMTP_SERVER, SMTP_PORT)
    smtp.login(SMTP_SENDER_EMAIL, SMTP_PASSWORD)

    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = SMTP_SENDER_EMAIL
    message["To"] = to_email

    text = message_text
    html = """\
                <html>
                  <body>
                    <h1>ELS-Einsatzinfo FF Alkoven</h1>
                    <p>%s
                    </p>
                  </body>
                </html>
                """ % message_html
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")
    message.attach(part1)
    message.attach(part2)
    smtp.sendmail(SMTP_SENDER_EMAIL, to_email, message.as_string())
    smtp.quit()


def sendmailToAllReceipients(subject, operation):
    receipients = ['kommandant@feuerwehr-alkoven.at',
                   '1.kdtstv@feuerwehr-alkoven.at',
                   '2.kdtstv@feuerwehr-alkoven.at',
                   'admin@feuerwehr-alkoven.at',
                   'monika.rainer@alkoven.ooe.gv.at']
    # receipients = ['gerald@zukrigl.at',  'admin@feuerwehr-alkoven.at']
    subject = subject % operation.id
    print("send mail: " + str(subject))
    print(operation.toString())
    for receipient in receipients:
        print("--> %s" % receipient)
        sendEmail(receipient,
                  subject,
                  operation.toString(),
                  operation.toHtml())


def log2file(data):
    f = open("log.txt", "a")
    f.write(data)
    f.close()
    pass


count_order_list = 0
active_operations = {}


class Operation(object):
    id = ''
    level = ''
    name = ''
    operationName = ''
    location = ''
    info = ''
    caller = ''
    program = ''
    status = ''
    receiveTad = ''
    watchOutTad = ''
    finishedTad = ''

    def __init__(self, xmlOrder):
        for field in xmlOrder:
            if field.tag == "operation-id":
                self.id = field.text
            elif field.tag == "level":
                self.level = field.text
            elif field.tag == "name":
                self.name = field.text
            elif field.tag == "operation-name":
                self.operationName = field.text
            elif field.tag == "location":
                self.location = field.text
            elif field.tag == "info":
                self.info = field.text
            elif field.tag == "caller":
                self.caller = field.text
            elif field.tag == "program":
                self.program = field.text
            elif field.tag == "status":
                self.status = field.text
            elif field.tag == "receive-tad":
                selfreceiveTad = field.text
            elif field.tag == "watch-out-tad":
                self.watchOutTad = field.text
            elif field.tag == "finished-tad":
                self.finishedTad = field.text

    def field(self, label, value):
        if value is None:
            return ""
        return label + ':' + ' ' * (40 - len(label)) + value + '\r\n'

    def fieldHtml(self, label, value):
        if value is None:
            return ""
        return '<tr><td>%s</td><td>%s</td></tr>' % (label, value)

    def toString(self):
        result = self.field('Einsatz', self.id)
        result += self.field('Einsatzort', self.location)
        result += self.field('Alarmstichwort', self.operationName)
        result += self.field('Alarmtext', self.info)
        result += self.field('Hausname', self.name)
        result += self.field('Alarmstufe', self.level)
        result += self.field('Anrufertelefonnummer', self.caller)
        result += self.field('Sirenenprogramm', self.program)
        result += self.field('Alarmstatus:', self.status)
        result += self.field('Alarmiert um:', self.receiveTad)
        result += self.field('Ausgerückt um:', self.watchOutTad)
        result += self.field('Eingerückt um:', self.finishedTad)
        return result

    def toHtml(self):
        result = '<h2>Einsatz: %s</h2>' % (self.id)
        result += '<table style="border:1px solid black;">'
        result += self.fieldHtml('Einsatzort', self.location)
        result += self.fieldHtml('Alarmstichwort', self.operationName)
        result += self.fieldHtml('Alarmtext', self.info)
        result += self.fieldHtml('Hausname', self.name)
        result += self.fieldHtml('Alarmstufe', self.level)
        result += self.fieldHtml('Anrufertelefonnummer', self.caller)
        result += self.fieldHtml('Sirenenprogramm', self.program)
        result += self.fieldHtml('Alarmstatus:', self.status)
        result += self.fieldHtml('Alarmiert um:', self.receiveTad)
        result += self.fieldHtml('Ausgerückt um:', self.watchOutTad)
        result += self.fieldHtml('Eingerückt um:', self.finishedTad)
        result += '</table>'
        return result


def processOperation(data):
    global active_operations
    # log2file(data)
    try:
        xml_tree = ET.fromstring(data)
    except ET.ParseError:
        return
    current_operations = {}
    for orderList in xml_tree.findall('order-list'):
        for order in orderList:
            operation = Operation(order)
            active_operation = active_operations.get(operation.id)
            if active_operation is None:
                print("new operation %s" % operation.id)
                sendmailToAllReceipients("Neuer Einsatz %s", operation)
            elif active_operation.status != operation.status:
                print("operation %s changed status from %s to %s" %
                      (operation.id,
                       active_operation.status,
                       operation.status))
                sendmailToAllReceipients("Ausgerückt %s", operation)
            current_operations[operation.id] = operation
            # print(operation.toString())
    for active_operation_id in active_operations.keys():
        if active_operation_id not in current_operations.keys():
            print("operation %s closed" % active_operation_id)
            operation = active_operations[active_operation_id]
            operation.status = 'Eingerückt'
            operation.finishedTad = time.strftime("%Y-%m-%d %H:%M:%S",
                                                  time.localtime())
            sendmailToAllReceipients("Eingerückt %s", operation)
    active_operations = current_operations


def readSocket():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(b'get-alarms')
        endloop = 0
        while endloop == 0:
            log2file(time.strftime('%Y-%m-%d %H:%M:%S\r\n', time.localtime()))
            heartbeat.sendHeartBeat()
            time.sleep(5)
            data = b""
            try:
                data = s.recv(4096)
            except IOError as e:
                print(e)
                endloop = 1
                data = b""
            data = data.decode("iso-8859-15")
            # zuk: 20200103 print ("data: " + data)
            if len(data) > 0:
                # zuk: 20200103 log2file(data)
                processOperation(data)
            else:
                print("data empty --> ending recvloop")
                endloop = 1
        s.close()


while True:
    readSocket()

exit()

testdata = [
    """<pdu>
            <order-list count="1">
                <order index="1">
                        <key>0x016d48b8</key>
                        <origin tid="0000000">LFKOO</origin>
                        <receive-tad>2019-11-06 17:58:49</receive-tad>
                        <operation-id>E191100458</operation-id>
                        <level>1</level>
                        <name>TEST</name>
                        <operation-name>TEST WAS-ENDSTELLE 1</operation-name>
                        <caller></caller>
                        <location>Altensam 1 Pühret Pühret</location>
                        <info>TEST</info>
                        <program>Stiller Alarm oHT</program>
                        <status>Alarmiert</status>
                        <watch-out-tad></watch-out-tad>
                        <finished-tad></finished-tad>
                        <destination-list count="1">
                        <destination index="1" id="34101">ALKOVEN</destination>
                        </destination-list>
                        <paging-destination-list count="0">
                        </paging-destination-list>
                </order>
            </order-list>
    </pdu>""",
    """<pdu>
                <order-list count="1">
                    <order index="1">
                        <key>0x016d48b8</key>
                        <origin tid="0000000">LFKOO</origin>
                        <receive-tad>2019-11-06 17:58:49</receive-tad>
                        <operation-id>E191100458</operation-id>
                        <level>1</level>
                        <name>TEST</name>
                        <operation-name>TEST WAS-ENDSTELLE 1</operation-name>
                        <caller></caller>
                        <location>Altensam 1 Pühret Pühret</location>
                        <info>TEST</info>
                        <program>Stiller Alarm oHT</program>
                        <status>Ausgerückt</status>
                        <watch-out-tad>2019-11-06 17:59:02</watch-out-tad>
                        <finished-tad></finished-tad>
                        <destination-list count="1">
                        <destination index="1" id="34101">ALKOVEN</destination>
                        </destination-list>
                        <paging-destination-list count="0">
                        </paging-destination-list>
                </order>
            </order-list>
    </pdu>""",
    """<pdu>
                <order-list count="2">
                    <order index="1">
                        <key>0x016d48b8</key>
                        <origin tid="0000000">LFKOO</origin>
                        <receive-tad>2019-11-06 17:58:49</receive-tad>
                        <operation-id>E191100458</operation-id>
                        <level>1</level>
                        <name>TEST</name>
                        <operation-name>TEST WAS-ENDSTELLE 1</operation-name>
                        <caller></caller>
                        <location>Altensam 1 Pühret Pühret</location>
                        <info>TEST</info>
                        <program>Stiller Alarm oHT</program>
                        <status>Ausgerückt</status>
                        <watch-out-tad>2019-11-06 17:59:02</watch-out-tad>
                        <finished-tad></finished-tad>
                        <destination-list count="1">
                        <destination index="1" id="34101">ALKOVEN</destination>
                        </destination-list>
                        <paging-destination-list count="0">
                        </paging-destination-list>
                </order>
                <order index="2">
                        <key>0x016d48b8</key>
                        <origin tid="0000000">LFKOO</origin>
                        <receive-tad>2019-11-06 17:58:49</receive-tad>
                        <operation-id>E191100476</operation-id>
                        <level>1</level>
                        <name>TEST</name>
                        <operation-name>TEST WAS-ENDSTELLE Zwo</operation-name>
                        <caller>069910149977</caller>
                        <location>Altensam 1 Pühret Pühret</location>
                        <info>TEST</info>
                        <program>Stiller Alarm oHT</program>
                        <status>Alarmiert</status>
                        <watch-out-tad></watch-out-tad>
                        <finished-tad></finished-tad>
                        <destination-list count="1">
                        <destination index="1" id="34101">ALKOVEN</destination>
                        </destination-list>
                        <paging-destination-list count="0">
                        </paging-destination-list>
                </order>
            </order-list>
    </pdu>""",
    """<pdu>
                <order-list count="2">
                    <order index="1">
                        <key>0x016d48b8</key>
                        <origin tid="0000000">LFKOO</origin>
                        <receive-tad>2019-11-06 17:58:49</receive-tad>
                        <operation-id>E191100458</operation-id>
                        <level>1</level>
                        <name>TEST</name>
                        <operation-name>TEST WAS-ENDSTELLE</operation-name>
                        <caller></caller>
                        <location>Altensam 1 Pühret Pühret 1</location>
                        <info>TEST</info>
                        <program>Stiller Alarm oHT</program>
                        <status>Ausgerückt</status>
                        <watch-out-tad>2019-11-06 17:59:02</watch-out-tad>
                        <finished-tad></finished-tad>
                        <destination-list count="1">
                        <destination index="1" id="34101">ALKOVEN</destination>
                        </destination-list>
                        <paging-destination-list count="0">
                        </paging-destination-list>
                </order>
                <order index="2">
                        <key>0x016d48b8</key>
                        <origin tid="0000000">LFKOO</origin>
                        <receive-tad>2019-11-06 17:58:49</receive-tad>
                        <operation-id>E191100476</operation-id>
                        <level>1</level>
                        <name>TEST</name>
                        <operation-name>TEST WAS-ENDSTELLE</operation-name>
                        <caller>069910149977</caller>
                    <location>Altensam 1 Pühret Pühret Zwo</location>
                        <info>TEST</info>
                        <program>Stiller Alarm oHT</program>
                        <status>Ausgerückt</status>
                        <watch-out-tad>2019-11-06 17:59:02</watch-out-tad>
                        <finished-tad></finished-tad>
                        <destination-list count="1">
                        <destination index="1" id="34101">ALKOVEN</destination>
                        </destination-list>
                        <paging-destination-list count="0">
                        </paging-destination-list>
                </order>
            </order-list>
    </pdu>""",
    """<pdu>
        <order-list count="1">
            <order index="1">
                <key>0x016d48b8</key>
                <origin tid="0000000">LFKOO</origin>
                <receive-tad>2019-11-06 17:58:49</receive-tad>
                <operation-id>E191100476</operation-id>
                <level>1</level>
                <name>TEST</name>
                <operation-name>TEST WAS-ENDSTELLE Zwo</operation-name>
                <caller>069910149977</caller>
                <location>Altensam 1 Pühret Pühret</location>
                <info>TEST</info>
                <program>Stiller Alarm oHT</program>
                <status>Ausgerückt</status>
                <watch-out-tad>2019-11-06 17:59:02</watch-out-tad>
                <finished-tad></finished-tad>
                <destination-list count="1">
                <destination index="1" id="34101">ALKOVEN</destination>
                </destination-list>
                <paging-destination-list count="0">
                </paging-destination-list>
            </order>
        </order-list>
    </pdu>""",
    """<pdu>
            <order-list count="0">
            </order-list>
    </pdu>"""
]

i = 0
for data in testdata:
    i += 1
    processOperation(data)
