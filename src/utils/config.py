import json

class Config:
    _config = None

    @classmethod
    def read_config(cls):
        if cls._config is None:
            with open('appsettings.json', 'r') as file:
                cls._config = json.loads(file.read())
        return cls._config

CONFIG = Config.read_config()