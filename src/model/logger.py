from datetime import datetime
import os
import inspect
from model.Config import Config

class Log:

    def __init__(
        self, message, debug=False, disposable=False, default_file_path_logging=False
    ):
        self.time = datetime.now()
        self.debug = debug
        self.disposable = disposable
        self.default_file_path_logging = default_file_path_logging
        try:
            self.message = str(message)
        except Exception as exception:
            self.message = ""
            Logger.log(exception, debug=False, disposable=True)

    def __str__(self):
        return str(self.time) + ": " + self.message


class Logger:

    console_logging_enabled = True
    file_logging_enabled = True
    debug_logging_enabled = True

    default_log_folder_path_name = "logs\\"
    program_path = os.path.realpath(__file__)
    program_dir_path = os.path.dirname(program_path)
    default_log_folder_path = os.path.join(
        program_dir_path, default_log_folder_path_name
    )

    def __init__(self, config:Config):
        self.set_log_config(config)

    def set_default_log_folder_path(
        self, __file, default_log_folder_path_name="logs\\"
    ):
        program_path = os.path.realpath(__file)
        program_dir_path = os.path.dirname(program_path)
        self.default_log_folder_path = os.path.join(
            program_dir_path, default_log_folder_path_name
        )

    def log(
        self, message, debug=False, disposable=False, default_file_path_logging=False
    ):
        log = Log(
            message=message,
            debug=debug,
            disposable=disposable,
            default_file_path_logging=default_file_path_logging,
        )
        if (debug and self.debug_logging_enabled) or not debug:
            if self.console_logging_enabled:
                self.console_logging(log)
            if self.file_logging_enabled:
                self.file_logging(log, self.get_log_file_path())
                if default_file_path_logging:
                    self.file_logging(log, self.get_default_log_file_path())

    def console_logging(self, log):
        try:
            print(str(log))
        except Exception as exception:
            if not log.disposable:
                self.log(
                    f"console logging error: {exception}", debug=False, disposable=True
                )

    def file_logging(self, log: Log, file_path):
        try:
            log_directory_path = os.path.dirname(file_path)
            if not os.path.isdir(log_directory_path):
                os.makedirs(log_directory_path, exist_ok=True)
            with open(file_path, "a+") as log_file:
                print(str(log), file=log_file)
        except Exception as exception:
            if not log.disposable:
                self.log(
                    log.message,
                    debug=False,
                    disposable=True,
                    default_file_path_logging=True,
                )
                self.log(
                    f"file logging error: {exception}",
                    debug=False,
                    disposable=True,
                    default_file_path_logging=True,
                )

    def get_default_log_file_path(self):
        current_time = datetime.now()
        # file_name = f"{logger.log_folder_path}/log_{current_time.year}{current_time.month}{current_time.day}.log"
        file_name = f"{current_time.strftime("%Y%m%d")}.log"
        return os.path.join(self.default_log_folder_path, file_name)

    def get_log_file_path(self):
        current_time = datetime.now()
        log_file_name = f"{current_time.strftime("%Y%m%d")}.log"
        # return f"{logger.log_folder_path}/log_{current_time.year}{current_time.month}{current_time.day}.log"
        return os.path.join(self.log_folder_path, log_file_name)

    def set_log_config(self, config:Config):
        self.console_logging_enabled = config.log_config.console_logging_enabled
        self.file_logging_enabled = config.log_config.file_logging_enabled
        self.debug_logging_enabled = config.log_config.debug_logging_enabled
        self.log_folder_path = config.log_config.Path_log_folder_path

