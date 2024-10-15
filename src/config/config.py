from json import load, dump


def get_config(config_path):
    with open(config_path, "r") as config_file:
        return load(config_file)
