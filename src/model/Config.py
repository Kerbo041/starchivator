from json import load


class Config:

    TOTAL_NUMBER_OF_VALUES = 200000
    TOTAL_NUMBER_OF_ANALOG_VALUES = 200000
    TOTAL_NUMBER_OF_DISCRETE_VALUES = 200000
    BLOCK_NUMBER = 3
    
    def __init__(self, config_path):
        self.config_path = config_path
        self.read_config_file(self.config_path)

    def read_config_file(self, config_path):
        with open(config_path) as config_file:
            config = load(config_file)

            file_paths = config["Paths"]
            headers = config["HeaderTexts"]
            log_config = config["Logs"]

            self.file_paths = ConfigFilePaths(file_paths)
            self.header_texts = ConfigHeaderTexts(headers)
            self.log_config = ConfigLogs(log_config)


class ConfigProgramParameters:
    def __init__(self, raw_config_dict):
        self.total_number_of_values = int(raw_config_dict["total_number_of_values"])
        self.total_number_of_analog_values =int(raw_config_dict["total_number_of_analog_values"])
        self.total_number_of_values = int(raw_config_dict["total_number_of_values"])
        self.block_number = int(raw_config_dict["block_number"])

class ConfigFilePaths:

    def __init__(self, raw_config_dict):
        self.path_out_dat = raw_config_dict["Path_out_dat"]
        self.path_x_dat = raw_config_dict["Path_x_dat"]
        self.path_out_0 = raw_config_dict["Path_out_0"]
        self.path_out_1 = raw_config_dict["Path_out_1"]
        self.path_arc_folder = raw_config_dict["Path_arc_folder"]


class ConfigHeaderTexts:

    def __init__(self, raw_config_dict):
        self.headerTexts = raw_config_dict["HeaderTexts"]
        self.out_dat = raw_config_dict["OutDat"]
        self.x_dat = raw_config_dict["XDat"]
        self.archive = raw_config_dict["Archive"]


class ConfigLogs:

    def __init__(self, raw_config_dict):
        self.console_logging_enabled = raw_config_dict["console_logging_enabled"]
        self.file_logging_enabled = raw_config_dict["file_logging_enabled"]
        self.debug_logging_enabled = raw_config_dict["debug_logging_enabled"]
        self.Path_log_folder_path = raw_config_dict["Path_log_folder_path"]
