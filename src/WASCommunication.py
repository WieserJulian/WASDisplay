#  *******************************************************
#   * Copyright (C) 2023 Julian Wieser
#   * julian.wieser@i-wieser.com
#   *
#   * This project can not be copied and/or distributed without the express
#   * permission of Julian Wieser
#   *******************************************************
import socket
import time
import xml.etree.ElementTree as ET

from src.Emergency import Emergency
from src.TestData import get_testDataGenerator

HOST = '192.168.130.100'
PORT = 47000


class WASCommunication:
    def __init__(self, root, DEBUG):
        self.root = root
        self.count_order_list = 0
        self.active_operations = {}
        self.DEBUG = DEBUG
        if not DEBUG:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, PORT))
                s.sendall(b'get-alarms')
                self.socket = s

    def readSocket(self):
        """ Single Read """
        if self.DEBUG:
            for data in get_testDataGenerator(1):
                self.processOperation(data)
            return
        data = b""
        try:
            data = self.socket.recv(4096)
        except IOError as e:
            print(e)
            data = b""
        data = data.decode("iso-8859-15")
        # zuk: 20200103 print ("data: " + data)
        if len(data) > 0:
            # zuk: 20200103 log2file(data)
            self.processOperation(data)
        else:
            print("data empty --> ending recvloop")


    def processOperation(self, data):
        # log2file(data)
        try:
            xml_tree = ET.fromstring(data)
        except ET.ParseError:
            return
        current_operations = {}
        for orderList in xml_tree.findall('order-list'):
            for order in orderList:
                operation = Emergency(order)
                active_operation = self.active_operations.get(operation.id)
                if active_operation is None:
                    print("new operation %s" % operation.id)
                elif active_operation.status != operation.status:
                    print("operation %s changed status from %s to %s" %
                          (operation.id,
                           active_operation.status,
                           operation.status))
                current_operations[operation.id] = operation
                # print(operation.toString())
        for active_operation_id in self.active_operations.keys():
            if active_operation_id not in current_operations.keys():
                print("operation %s closed" % active_operation_id)
                operation = self.active_operations[active_operation_id]
                operation.status = 'Eingerückt'
                operation.finishedTad = time.strftime("%Y-%m-%d %H:%M:%S",
                                                      time.localtime())
        self.active_operations = current_operations
        self.root.event_generate("<<WASCommunication>>")
