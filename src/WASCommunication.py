#  *******************************************************
#   * Copyright (C) 2023 Julian Wieser
#   * julian.wieser@i-wieser.com
#   *
#   * This project can not be copied and/or distributed without the express
#   * permission of Julian Wieser
#   *******************************************************
import math
import socket
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
        print("[*] Start trying to read Socket")
        data = b""
        try:
            if not self.DEBUG:
                self.client.send(b'get-alarms')
            data = self.client.recv(4096)
        except ConnectionError:
            print("[!] Couldnt connect retry")
            self.reconnect()
            return
        except IOError as e:
            print("[!] some errror:"+e)
            print(e)
            data = b""
        except:
            print("[!] Unexpexted Error")
        data = data.decode("iso-8859-15")
        # zuk: 20200103 print ("data: " + data)
        if len(data) > 0:
            # zuk: 20200103 log2file(data)
            self.processOperation(data)
        else:
            print("data empty --> ending recvloop")

    def reconnect(self):
        if not self.DEBUG:
            self.socket.bind((self.config.server['host'], self.config.server['port']))
            print(f"[*] Listening as {self.config.server['host']}:{self.config.server['port']}")
        else:
            self.socket.bind((self.config.server['debug_host'], self.config.server['debug_port']))
            print(f"[*] Listening as {self.config.server['debug_host']}:{self.config.server['debug_port']}")
        self.socket.listen(5)
        self.client, address = self.socket.accept()
        print(f"[+] {address} is connected.")

    def processOperation(self, data):
        # log2file(data)
        print("[+] Start Processing Operations")
        if data is None:
            print("[!] Data is None")
            return
        try:
            xml_tree = ET.fromstring(data)
        except ET.ParseError:
            print("[!] ET Parse ERROR")
            return
        current_operations = {}
        for orderList in xml_tree.findall('order-list'):
            for order in orderList:
                operation = Emergency(order)

                active_operation = self.active_operations.get(operation.id)
                if active_operation is None:
                    print("new operation %s" % operation.id)
                    s = time.time()
                    # operation.navigation_Figure = self.generate_image(operation)
                    print(time.time() - s)
                    print(operation.toString())
                elif active_operation.status != operation.status:
                    print("operation %s changed status from %s to %s" %
                          (operation.id,
                           active_operation.status,
                           operation.status))
                current_operations[operation.id] = operation
        for active_operation_id in self.active_operations.keys():
            if active_operation_id not in current_operations.keys():
                print("operation %s closed" % active_operation_id)
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
        s = time.time()
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

        print("generate ", time.time() - s)

        s = time.time()

        fig, ax = self.config.generated_plot

        fig, ax = ox.plot_graph_route(self.config.g_drive, route, ax=ax, show=False, route_color="#5AAFFB",
                                      route_linewidth=6, bbox=bbox)
        fig, ax = ox.plot_graph(self.config.g_drive, ax=ax, show=True, bbox=bbox)
        print("draw ", time.time() - s)
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
