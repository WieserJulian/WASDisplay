#  *******************************************************
#   * Copyright (C) 2023 Julian Wieser
#   * julian.wieser@i-wieser.com
#   *
#   * This project can not be copied and/or distributed without the express
#   * permission of Julian Wieser
#   *******************************************************
import logging
import math
import socket
import threading
import time
import xml.etree.ElementTree as ET

import osmnx.distance
import osmnx as ox

from src.Emergency import Emergency
from src.TestData import get_testDataGenerator
from src.config import Config


class WASCommunication:
    def __init__(self, root, DEBUG):
        self.client = None
        self.root = root
        self.count_order_list = 0
        self.active_operations = {}
        self.DEBUG = DEBUG
        self.config = Config()
        self.socket = socket.socket()
        self.reconnect()

    def readSocket(self):
        """ Single Read """
        logging.debug("[*] Start trying to read Socket")
        data = b""
        if self.client is None:
            logging.error("[!] Client not accepted")
            return
        try:
            if not self.DEBUG:
                self.client.send(b'get-alarms')
            data = self.client.recv(8192)
        except ConnectionError:
            logging.error("[!] Couldnt connect retry")
            self.reconnect()
            return
        except IOError as e:
            logging.error("[!] some errror:", e)
            data = b""
        except:
            logging.error("[!] Unexpexted Error")
        data = data.decode("iso-8859-15")
        # zuk: 20200103 print ("data: " + data)
        if len(data) > 0:
            # zuk: 20200103 log2file(data)
            self.processOperation(data)
        else:
            logging.debug("data empty --> ending recvloop")

    def reconnect(self):
        if not self.DEBUG:
            self.socket.bind((self.config.server['host'], self.config.server['port']))
            logging.debug(f"[*] Listening as {self.config.server['host']}:{self.config.server['port']}")
        else:
            self.socket.bind((self.config.server['debug_host'], self.config.server['debug_port']))
            logging.debug(f"[*] Listening as {self.config.server['debug_host']}:{self.config.server['debug_port']}")
        self.socket.listen(5)
        threading.Thread(target=self.wait_for_accept).start()

    def wait_for_accept(self):
        self.client, address = self.socket.accept()
        logging.debug(f"[+] {address} is connected.")

    def processOperation(self, data):
        # log2file(data)
        logging.debug("[+] Start Processing Operations")
        if data is None:
            logging.error("[!] Data is None")
            return
        try:
            xml_tree = ET.fromstring(data)
        except ET.ParseError:
            logging.error("[!] ET Parse ERROR", data)
            return
        current_operations = {}
        for orderList in xml_tree.findall('order-list'):
            for order in orderList:
                operation = Emergency(order)

                active_operation = self.active_operations.get(operation.id)
                if active_operation is None:
                    logging.debug("new operation %s" % operation.id)
                    s = time.time()
                    # operation.navigation_Figure = self.generate_image(operation)
                    logging.debug(operation.toString())
                elif active_operation.status != operation.status:
                    logging.debug("operation %s changed status from %s to %s" %
                          (operation.id,
                           active_operation.status,
                           operation.status))
                current_operations[operation.id] = operation
        for active_operation_id in self.active_operations.keys():
            if active_operation_id not in current_operations.keys():
                logging.debug("operation %s closed" % active_operation_id)
                operation = self.active_operations[active_operation_id]
                operation.status = 'Eingerückt'
                operation.finishedTad = time.strftime("%Y-%m-%d %H:%M:%S",
                                                      time.localtime())
        self.active_operations = current_operations
        self.root.event_generate("<<WASCommunication>>")

    def generate_image(self, emergency: Emergency):
        tags = {"building": True}
        gdf_depo = self.config.gdf_depo
        gdf_emergency = ox.features_from_place(emergency.location + " AUSTRIA", tags)
        dist = int(self.distance((gdf_depo.centroid.x.values, gdf_depo.centroid.y.values),
                                 (gdf_emergency.centroid.x.values, gdf_emergency.centroid.y.values)) * 1000) + 500
        middle_point = (((gdf_depo.centroid.x.values + gdf_emergency.centroid.x.values) / 2)[0],
                        ((gdf_depo.centroid.y.values + gdf_emergency.centroid.y.values) / 2)[0])

        middle_point_ox = osmnx.distance.Point((middle_point[1], middle_point[0]))

        bbox = ox.utils_geo.bbox_from_point((middle_point_ox.x, middle_point_ox.y), dist=int(dist / 2))

        emergency_way, _ = ox.nearest_nodes(self.config.g_overview, gdf_emergency.centroid.x.values,
                                            gdf_emergency.centroid.y.values,
                                            return_dist=True)

        route = ox.shortest_path(self.config.g_drive, self.config.depo_way[0], emergency_way[0], weight="length")

        fig, ax = self.config.generated_plot

        fig, ax = ox.plot_graph_route(self.config.g_drive, route, ax=ax, show=False, route_color="#5AAFFB",
                                      route_linewidth=6, bbox=bbox)
        fig, ax = ox.plot_graph(self.config.g_drive, ax=ax, show=True, bbox=bbox)
        return fig

    def generate_bevorehand(self, g_overview, gdf_depo, gdf_emergency, tags):

        return

    def distance(self, origin, destination):
        lat1, lon1 = origin
        lat2, lon2 = destination
        radius = osmnx.distance.EARTH_RADIUS_M / 1000  # km

        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(math.radians(lat1)) \
            * math.cos(math.radians(lat2)) * math.sin(dlon / 2) * math.sin(dlon / 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        d = radius * c

        return d
