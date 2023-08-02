import math
import osmnx.distance
from customtkinter import CTkFrame
import osmnx as ox


class NavigationFrame(CTkFrame):
    def __init__(self, master, emergency_address: str, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color ="red")
        self.generate_image(emergency_address)
        self.place_depo = "Bach 49, Rutzenham, Austria"

    def generate_image(self, emergency_address):
        pass
        osmnx.distance.Point()

    def get_nearest_middle_node(self, gdf_depo, gdf_emergency):
        dist = int(self.distance((gdf_depo.centroid.x.values, gdf_depo.centroid.y.values),
                            (gdf_emergency.centroid.x.values, gdf_emergency.centroid.y.values)) * 1000)
        middle_point = (((gdf_depo.centroid.x.values + gdf_emergency.centroid.x.values) / 2)[0],
                        ((gdf_depo.centroid.y.values + gdf_emergency.centroid.y.values) / 2)[0])
        G_overview = ox.graph_from_address(self.place_depo, dist=dist, simplify=True, retain_all=True, network_type="all")
        middle_node = ox.nearest_nodes(G_overview, middle_point[0], middle_point[1])
        G_middle_drive = ox.graph_from_point((middle_node["x"], middle_node["y"]), network_type="drive",
                                             dist=int(dist / 2))
        G_middle_overview = ox.graph_from_point((middle_node["x"], middle_node["y"]), network_type="drive",
                                                dist=int(dist / 2))
        return G_middle_drive, G_middle_overview

    def distance(origin, destination):
        lat1, lon1 = origin
        lat2, lon2 = destination
        radius = osmnx.distance.EARTH_RADIUS_M / 1000 # km

        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(math.radians(lat1)) \
            * math.cos(math.radians(lat2)) * math.sin(dlon / 2) * math.sin(dlon / 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        d = radius * c

        return d