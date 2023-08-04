#  *******************************************************
#   * Copyright (C) 2023 Julian Wieser
#   * julian.wieser@i-wieser.com
#   *
#   * This project can not be copied and/or distributed without the express
#   * permission of Julian Wieser
#   *******************************************************
import time

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
                        <location>BACH 4 RUTZENHAM RUTZENHAM</location>
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
                        <location>BACH 4 RUTZENHAM RUTZENHAM</location>
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
                        <location>BACH 4 RUTZENHAM RUTZENHAM</location>
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
                        <location>BACH 4 RUTZENHAM RUTZENHAM</location>
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
global i
i = 0
def get_testDataGenerator(wait_time: float):
    global i
    if i == len(testdata):
        i = 0
        # return
    i += 1
    return testdata[i - 1]
    # while True:
    # yield testdata[i]
    # time.sleep(wait_time)
    #     i += 1
    #     if i == len(testdata):
    #         i = 0