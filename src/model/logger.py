from datetime import datetime
import os


class logger:

    console_logging_enabled = True
    file_logging_enabled = True
    debug_logging_enabled = True
    short_log_folder_path = "logs/"

    # def __init__(self, logs_config):
    #     self.console_logging_enabled = logs_config["console_logging_enabled"]
    #     self.file_logging_enabled = logs_config["file_logging_enabled"]
    #     self.debug_logging_enabled = logs_config["debug_logging_enabled"]
    #     self.short_logging_enabled = logs_config["short_logging_enabled"]
    #     self.debug_log_folder_path = logs_config["debug_log_folder_path"]
    #     self.short_log_folder_path = logs_config["short_log_folder_path"]

    def log(message, debug = False, disposable=False):
        if debug and logger.debug_logging_enabled:
            logger.make_log(message, debug, disposable)
        elif not debug:
            logger.make_log(message, debug, disposable)

    def make_log(message, debug, disposable):
        if logger.console_logging_enabled:
            logger.console_logging(message, disposable)
        if logger.file_logging_enabled:
            logger.file_logging(message, logger.get_log_file_path(), disposable)

    def console_logging(message, disposable = False):
        try:
            print(f"{datetime.now()}:\t{message}")
        except Exception as exception:
            if not disposable:
                logger.log(f"console logging error: {exception}", debug= False, disposable=True)

    def file_logging(message, file_path, disposable = False):
        try:
            log_directory_path = os.path.dirname(file_path)
            if not os.path.isdir(log_directory_path):
                os.makedirs(log_directory_path, exist_ok=True)
            with open(file_path, "a+") as log_file:
                print(f"{datetime.now()}:\t{message}", file=log_file)
        except Exception as exception:
            if not disposable:
                logger.log(f"file logging error: {exception}", debug= False, disposable=True)

    def get_log_file_path():
        current_time = datetime.now()
        return f"{logger.short_log_folder_path}/log_{current_time.year}{current_time.month}{current_time.day}.log"

    def set_log_config(logs_config):
        logger.console_logging_enabled = logs_config["console_logging_enabled"]
        logger.file_logging_enabled = logs_config["file_logging_enabled"]
        logger.debug_logging_enabled = logs_config["debug_logging_enabled"]
        logger.short_log_folder_path = logs_config["Path_log_folder_path"]

    # old code
    def short_log(message):
        try:
            if type(message) is not str:
                message = str(message)
            if logger.console_logging_enabled:
                logger.console_logging(message)
            if logger.file_logging_enabled:
                logger.file_logging(message, logger.get_log_file_path())
        except Exception as exception:
            print(exception)

    def debug_log(message):
        try:
            if logger.debug_logging_enabled:
                if type(message) is not str:
                    message = str(message)
                if logger.console_logging_enabled:
                    logger.console_logging(message)
                if logger.file_logging_enabled:
                    logger.file_logging(message, logger.get_log_file_path())
        except Exception as exception:
            print(exception)


# not in use
class Log:

    def __init__(self, message, debug=False, disposable=False):

        if debug(message) == str:
            self.message = message
        else:
            try:
                self.message = str(message)
            except Exception as exception:
                self.message = ""
                logger.log(exception, debug=False, disposable=True)
        self.type = debug
        self.disposable = disposable
