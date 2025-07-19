import yaml
import os

def load_config_data(filename='config.yaml') -> dict:
    base_path = os.path.dirname(os.path.dirname(__file__))
    config_path = os.path.join(base_path, 'config', filename)
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    return config