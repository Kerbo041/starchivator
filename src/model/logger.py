from datetime import datetime
import os
import inspect


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

    @classmethod
    def set_default_log_folder_path(cls, __file, default_log_folder_path_name="logs\\"):
        program_path = os.path.realpath(__file)
        program_dir_path = os.path.dirname(program_path)
        cls.default_log_folder_path = os.path.join(
            program_dir_path, default_log_folder_path_name
        )

    @classmethod
    def log(
        cls, message, debug=False, disposable=False, default_file_path_logging=False
    ):
        log = Log(
            message=message,
            debug=debug,
            disposable=disposable,
            default_file_path_logging=default_file_path_logging,
        )
        if (debug and cls.debug_logging_enabled) or not debug:
            if cls.console_logging_enabled:
                cls.console_logging(log)
            if cls.file_logging_enabled:
                cls.file_logging(log, cls.get_log_file_path())
                if default_file_path_logging:
                    cls.file_logging(log, cls.get_default_log_file_path())

    @classmethod
    def console_logging(cls, log):
        try:
            print(str(log))
        except Exception as exception:
            if not log.disposable:
                cls.log(
                    f"console logging error: {exception}", debug=False, disposable=True
                )

    @classmethod
    def file_logging(cls, log: Log, file_path):
        try:
            log_directory_path = os.path.dirname(file_path)
            if not os.path.isdir(log_directory_path):
                os.makedirs(log_directory_path, exist_ok=True)
            with open(file_path, "a+") as log_file:
                print(str(log), file=log_file)
        except Exception as exception:
            if not log.disposable:
                cls.log(
                    log.message,
                    debug=False,
                    disposable=True,
                    default_file_path_logging=True,
                )
                cls.log(
                    f"file logging error: {exception}",
                    debug=False,
                    disposable=True,
                    default_file_path_logging=True,
                )

    @classmethod
    def get_default_log_file_path(cls):
        current_time = datetime.now()
        # file_name = f"{logger.log_folder_path}/log_{current_time.year}{current_time.month}{current_time.day}.log"
        file_name = f"{current_time.strftime("%Y%m%d")}.log"
        return os.path.join(cls.default_log_folder_path, file_name)

    @classmethod
    def get_log_file_path(cls):
        current_time = datetime.now()
        log_file_name = f"{current_time.strftime("%Y%m%d")}.log"
        # return f"{logger.log_folder_path}/log_{current_time.year}{current_time.month}{current_time.day}.log"
        return os.path.join(cls.log_folder_path, log_file_name)

    @classmethod
    def set_log_config(cls, logs_config):
        cls.console_logging_enabled = logs_config["console_logging_enabled"]
        cls.file_logging_enabled = logs_config["file_logging_enabled"]
        cls.debug_logging_enabled = logs_config["debug_logging_enabled"]
        cls.log_folder_path = logs_config["Path_log_folder_path"]
