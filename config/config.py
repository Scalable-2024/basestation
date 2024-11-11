import json
import os

from config.constants import BASESTATION
from helpers.name_generator import generate_name

CONFIG_FILE_PATH = "config/config.json"

def load_from_config_file():
    # check if config file exists
    if os.path.exists(CONFIG_FILE_PATH):
        with open(CONFIG_FILE_PATH, "r") as config_file:
            return json.load(config_file)

    return create_config()

def create_config():
    config = {
        "name": generate_name(),
        "function": BASESTATION
    }

    with open(CONFIG_FILE_PATH, "w") as config_file:
        json.dump(config, config_file)

    return config