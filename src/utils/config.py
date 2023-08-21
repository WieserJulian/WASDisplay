import yaml
import osmnx as ox
import pickle

from geopandas import GeoDataFrame


class Config(object):
    def __init__(self, path: str = 'utils/config.yml'):
        with open(path, 'r') as file:
            self.__all_settings = yaml.safe_load(file)
            self.server = self.__all_settings['server']
            self.default = self.__all_settings['default']
            # if self.__all_settings['default']['init_addr'] == self.default['place_depo']:
            #     self.g_overview = ox.load_graphml("save/graph_overview")
            #     self.g_drive = ox.load_graphml("save/graph_drive")
            #     tags = {'building': True}
            #     self.gdf_depo = ox.features_from_place(self.default['place_depo'], tags)
            #     self.depo_way = self.__all_settings['default']['depo_way']
            #     with open('save/ax.pickle','rb') as fid:
            #         self.generated_plot = None, pickle.load(fid)
            # else:
            #     self.load_graphs()

    def load_graphs(self):
        self.g_overview = ox.graph_from_address(self.default['place_depo'], dist=15_000, network_type="all_private",
                                                simplify=False,
                                                retain_all=True)
        self.g_drive = ox.graph_from_address(self.default['place_depo'], dist=15_000, network_type="drive",
                                             simplify=False,
                                             retain_all=True)
        ox.save_graphml(self.g_overview, "save/graph_overview")
        ox.save_graphml(self.g_drive, "save/graph_drive")
        tags = {'building': True}
        self.gdf_depo = ox.features_from_place(self.default['place_depo'], tags)
        self.depo_way, _ = ox.nearest_nodes(self.g_overview, self.gdf_depo.centroid.x.values,
                                            self.gdf_depo.centroid.y.values,
                                            return_dist=True)
        _, ax = ox.plot_graph(self.g_overview, show=False, node_size=0, edge_linewidth=2, bgcolor='#F8F9FA',
                              node_color="#FFFFFF")
        _, ax = ox.plot_footprints(self.gdf_depo, ax=ax, alpha=1, show=False, color="g")

        gdf = ox.features_from_address(self.default['place_depo'], dist=15_000, tags=tags)
        self.generated_plot = ox.plot_footprints(gdf, ax=ax, alpha=0.5, show=False, color="b")
        pickle.dump(self.generated_plot[0], open('save/fig.pickle', 'wb'))
        pickle.dump(self.generated_plot[1], open('save/ax.pickle', 'wb'))
        with open('config.yml', 'w') as file:
            self.__all_settings['default']['init_addr'] = self.default['place_depo']
            self.__all_settings['default']['depo_way'] = self.depo_way
            _ = yaml.dump(self.__all_settings, file)

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Config, cls).__new__(cls)
        return cls.instance
