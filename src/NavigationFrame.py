import math
import time

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import osmnx.distance
from customtkinter import CTkFrame
import osmnx as ox

from src.Emergency import Emergency
from src.config import Config


class NavigationFrame(CTkFrame):
    def __init__(self, master, emergency: Emergency, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color ="red")
        self.emergency = emergency
        self.generate_image()

    def generate_image(self):
        g_overview = Config().g_overview

        tags = {"building": True}
        gdf_depo = ox.features_from_place(Config().default['place_depo'], tags)
        gdf_emergency = ox.features_from_place(self.emergency.location + " AUSTRIA", tags)
        s = time.time()
        G_middle_drive, G_middle_overview, gdf, route = self.get_nearest_middle_node(g_overview,gdf_depo, gdf_emergency, tags)
        print("generate ", time.time() - s)



        fig, ax = ox.plot_graph(G_middle_overview, show=False, node_size=0, edge_linewidth=2, bgcolor='#F8F9FA',
                                node_color="#FFFFFF")
        fig, ax = ox.plot_footprints(gdf_emergency, ax=ax, alpha=1, show=False, color="r")
        fig, ax = ox.plot_footprints(gdf_depo, ax=ax, alpha=1, show=False, color="g")
        fig, ax = ox.plot_footprints(gdf, ax=ax, alpha=0.5, show=False, color="b")
        fig, ax = ox.plot_graph_route(G_middle_drive, route, ax=ax,  show=False, route_color="#5AAFFB", route_linewidth=6)
        return fig

    def get_nearest_middle_node(self,g_overview, gdf_depo, gdf_emergency, tags):
        dist = int(self.distance((gdf_depo.centroid.x.values, gdf_depo.centroid.y.values),
                            (gdf_emergency.centroid.x.values, gdf_emergency.centroid.y.values)) * 1000) + 500
        middle_point = (((gdf_depo.centroid.x.values + gdf_emergency.centroid.x.values) / 2)[0],
                        ((gdf_depo.centroid.y.values + gdf_emergency.centroid.y.values) / 2)[0])

        # G_overview = ox.graph_from_address(Config().default['place_depo'], dist=dist, simplify=True, retain_all=True, network_type="all")
        # middle_node = ox.nearest_nodes(G_overview, middle_point[0], middle_point[1])
        #
        # middle_point_ox = osmnx.distance.Point((g_overview.nodes[middle_node]['y'], g_overview.nodes[middle_node]["x"]))

        middle_point_ox = osmnx.distance.Point(middle_point[1], middle_point[0])
        gdf = ox.features_from_point((middle_point_ox.x, middle_point_ox.y), dist=int(dist / 2), tags=tags)
        G_middle_drive = ox.graph_from_point((middle_point_ox.x, middle_point_ox.y), network_type="drive",
                                             dist=int(dist / 2))
        G_middle_overview = ox.graph_from_point((middle_point_ox.x, middle_point_ox.y), network_type="all_private",
                                                dist=int(dist / 2))
        depo_way, _ = ox.nearest_nodes(G_middle_drive, gdf_depo.centroid.x.values, gdf_depo.centroid.y.values,
                                       return_dist=True)
        emergency_way, _ = ox.nearest_nodes(G_middle_drive, gdf_emergency.centroid.x.values,
                                            gdf_emergency.centroid.y.values,
                                            return_dist=True)
        route = ox.shortest_path(G_middle_drive, depo_way[0], emergency_way[0], weight="length")

        return G_middle_drive, G_middle_overview, gdf, route

    def distance(self, origin, destination):
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