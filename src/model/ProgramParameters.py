from json import load


class ProgramParameters:

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


class ConfigFilePaths:

    def __init__(self, raw_config):
        self.Path_out_dat = raw_config["Path_out_dat"]
        self.Path_x_dat = raw_config["Path_x_dat"]
        self.Path_out_0 = raw_config["Path_out_0"]
        self.Path_out_1 = raw_config["Path_out_1"]
        self.Path_arc_folder = raw_config["Path_arc_folder"]


class ConfigHeaderTexts:

    def __init__(self, raw_config):
        self.HeaderTexts = raw_config["HeaderTexts"]
        self.OutDat = raw_config["OutDat"]
        self.XDat = raw_config["XDat"]
        self.Archive = raw_config["Archive"]


class ConfigLogs:

    def __init__(self, raw_config):
        self.console_logging_enabled = raw_config["console_logging_enabled"]
        self.file_logging_enabled = raw_config["file_logging_enabled"]
        self.debug_logging_enabled = raw_config["debug_logging_enabled"]
        self.Path_log_folder_path = raw_config["Path_log_folder_path"]
