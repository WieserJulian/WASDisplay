#  ******************************************************
#  * Copyright (C) 2023 Julian Wieser
#  * julian.wieser@i-wieser.com
#  *
#  * This project can not be copied and/or distributed without the express
#  * permission of Julian Wieser
#  *******************************************************
import math

import osmnx as ox


# place_depo = "Rutzenham, Austria"
# G = ox.graph_from_place(place_depo, network_type="drive", simplify=False)
#
# # get all the building footprints in a city
# gdf = ox.features_from_place("Rutzenham, Austria", {"building": True})
# gdf.shape
# # or plot street network and the geospatial features' footprints together
# fig, ax = ox.plot_footprints(gdf, alpha=1, show=False)
# fig, axw = ox.plot_graph(G, ax=ax, node_size=0, edge_color="w", edge_linewidth=0.7)
#
# pass
# place_depo = "Rutzenham, Austria"
# orig = list(G)[0]
# dest = list(G)[30]
# route = ox.shortest_path(G, orig, dest, weight="length")
# # get node colors by linearly mapping an attribute's values to a colormap
# nc = ox.plot.get_node_colors_by_attr(G, attr="y", cmap="plasma")
# fig, ax = ox.plot_graph(G, node_color=nc, edge_linewidth=0.3)
# # fig, ax = ox.plot_graph_route(G, route, route_color="y", route_linewidth=6, node_size=0)
# pass
# place_depo = "Bach 49, Rutzenham, Austria"
# place_emergency = "Bach 4, Rutzenham, Austria"
# tags = {"building": True}
# gdf_depo = ox.features_from_place(place_depo, tags)
# gdf_emergency = ox.features_from_place(place_emergency, tags)
# depo_way, _ = ox.nearest_nodes(G, gdf_depo.centroid.x.values, gdf_depo.centroid.y.values, return_dist=True)
# emergency_way, _ = ox.nearest_nodes(G, gdf_emergency.centroid.x.values, gdf_emergency.centroid.y.values, return_dist=True)
# route = ox.shortest_path(G, depo_way[0], emergency_way[0], weight="length")
# fig, ax = ox.plot_graph_route(G, route, route_color="y", route_linewidth=6, node_size=3)
# pass

def distance(origin, destination):
    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 6371  # km

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon / 2) * math.sin(dlon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = radius * c

    return d


# TODO
# Create a Distance between DEPO and EMERGENCY and then form the center of direct line make the map
# So all is inside these plot

G = ox.graph_from_place("Rutzenham, Austria", simplify=False)
place_depo = "Bach 49, Rutzenham, Austria"
place_emergency = "Altensham 1, Pühret, Austria"
tags = {"building": True}
gdf_depo = ox.features_from_place(place_depo, tags)
gdf_emergency = ox.features_from_place(place_emergency, tags)
# TODO Rework
depo_way, _ = ox.nearest_nodes(G, gdf_depo.centroid.x.values, gdf_depo.centroid.y.values, return_dist=True)
emergency_way, _ = ox.nearest_nodes(G, gdf_emergency.centroid.x.values, gdf_emergency.centroid.y.values,
                                    return_dist=True)
middle_point = (round(((gdf_depo.centroid.x.values + gdf_emergency.centroid.x.values) / 2)[0], 6),
                round(((gdf_depo.centroid.y.values + gdf_emergency.centroid.y.values) / 2)[0], 6))
dist = int(distance((gdf_depo.centroid.x.values, gdf_depo.centroid.y.values),
                    (gdf_emergency.centroid.x.values, gdf_emergency.centroid.y.values)) * 1000)
G_middle = ox.graph_from_address(place_depo, dist=dist, simplify=True, retain_all=True, network_type="drive")
gdf = ox.features_from_address(place_depo, dist=dist, tags={'building': True})
route = ox.shortest_path(G, depo_way[0], emergency_way[0], weight="length")
fig, ax = ox.plot_graph(G_middle, show=False, node_size=0, edge_linewidth=2)
fig, ax = ox.plot_footprints(gdf, ax=ax, alpha=0.4, show=False)
fig, ax = ox.plot_graph_route(G_middle, route, ax=ax, route_color="r", route_linewidth=6)
pass


def get_nearest_middle_node(gdf_depo, gdf_emergency):
    dist = int(distance((gdf_depo.centroid.x.values, gdf_depo.centroid.y.values),
                        (gdf_emergency.centroid.x.values, gdf_emergency.centroid.y.values)) * 1000)
    middle_point = (((gdf_depo.centroid.x.values + gdf_emergency.centroid.x.values) / 2)[0],
                    ((gdf_depo.centroid.y.values + gdf_emergency.centroid.y.values) / 2)[0])
    G_overview = ox.graph_from_address(place_depo, dist=dist, simplify=True, retain_all=True, network_type="all")
    middle_node = ox.nearest_nodes(G_overview, middle_point[0], middle_point[1])
    G_middle_drive = ox.graph_from_point((middle_node["x"], middle_node["y"]), network_type="drive", dist=int(dist/2))
    G_middle_overview = ox.graph_from_point((middle_node["x"], middle_node["y"]), network_type="drive", dist=int(dist/2))
    return G_middle_drive, G_middle_overview