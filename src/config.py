import yaml

class Config(object):
    def __init__(self):
        with open('config.yml', 'r') as file:
            self.__all_settings = yaml.safe_load(file)
            self.server = self.__all_settings['server']
            self.default = self.__all_settings['default']
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Config, cls).__new__(cls)
        return cls.instance
