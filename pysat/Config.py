import json
import os
from enum import Enum
import dacite
from dataclasses import dataclass
'''https://tech.preferred.jp/en/blog/working-with-configuration-in-python/'''


class Mode(Enum):
    SAT = 'SAT'
    GROUND = 'GROUND'


@dataclass
class Configuration:
    mode: Mode
    comm_device: str
    comm_baudrate: int
    gps_device: str
    gps_baudrate: int
    sat_temp_dir: str
    sat_final_dir: str
    downloaded_files_dir: str


class Config:
    _config_file = "config.json"
    _converters = {
        Mode: Mode,
    }
    _config_full_path = os.path.join(os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(_config_file))),
                                     _config_file)

    @staticmethod
    def get_config():
        with open(Config._config_full_path, "r") as file:
            raw_config = json.load(file)

        config = dacite.from_dict(data_class=Configuration, data=raw_config,
                                  config=dacite.Config(type_hooks=Config._converters))
        return config



