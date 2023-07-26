#  ******************************************************
#  * Copyright (C) 2023 Julian Wieser
#  * julian.wieser@i-wieser.com
#  *
#  * This project can not be copied and/or distributed without the express
#  * permission of Julian Wieser
#  *******************************************************
import numpy as np
import osmnx as ox
place_depo = "Rutzenham, Austria"
G = ox.graph_from_place(place_depo, network_type="drive", simplify=False)
orig = list(G)[0]
dest = list(G)[30]
route = ox.shortest_path(G, orig, dest, weight="length")
# fig, ax = ox.plot_graph_route(G, route, route_color="y", route_linewidth=6, node_size=0)
pass
place_depo = "Bach 49, Rutzenham, Austria"
place_emergency = "Bach 4, Rutzenham, Austria"
tags = {"building": True}
gdf_depo = ox.features_from_place(place_depo, tags)
gdf_emergency = ox.features_from_place(place_emergency, tags)
depo_way, _ = ox.nearest_nodes(G, gdf_depo.centroid.x.values, gdf_depo.centroid.y.values, return_dist=True)
emergency_way, _ = ox.nearest_nodes(G, gdf_emergency.centroid.x.values, gdf_emergency.centroid.y.values, return_dist=True)
route = ox.shortest_path(G, depo_way[0], emergency_way[0], weight="length")
fig, ax = ox.plot_graph_route(G, route, route_color="y", route_linewidth=6, node_size=3)
pass