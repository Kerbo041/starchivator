from datetime import datetime
import os

class logger():
    
    console_logging_enabled = True
    file_logging_enabled = True
    debug_logging_enabled = True
    short_logging_enabled = True
    debug_log_folder_path = "debug_logs/"
    short_log_folder_path= "logs/"
    
    # def __init__(self, logs_config):
    #     self.console_logging_enabled = logs_config["console_logging_enabled"]
    #     self.file_logging_enabled = logs_config["file_logging_enabled"]
    #     self.debug_logging_enabled = logs_config["debug_logging_enabled"]
    #     self.short_logging_enabled = logs_config["short_logging_enabled"]
    #     self.debug_log_folder_path = logs_config["debug_log_folder_path"]
    #     self.short_log_folder_path = logs_config["short_log_folder_path"]
    
    def any_log(message):
        logger.short_log(message)
        logger.debug_log(message)
    
    def short_log(message):
        if logger.short_logging_enabled:
            if type(message) is not str:
                message = str(message)
            if logger.console_logging_enabled:
                logger.console_logging(message)
            if logger.file_logging_enabled:
                logger.file_logging(message, logger.get_short_log_file_path())
    
    def debug_log( message):
        if logger.debug_logging_enabled:
            if type(message) is not str:
                message = str(message)
            if logger.console_logging_enabled:
                logger.console_logging(message)
            if logger.file_logging_enabled:
                logger.file_logging(message, logger.get_debug_log_file_path())
    
    def console_logging(message):
        print(f'{datetime.now()}:\t{message}')
        
    def file_logging(message, file_path):
        try:
            log_directory_path = os.path.dirname(file_path)
            if not os.path.isdir(log_directory_path):
                os.makedirs(log_directory_path, exist_ok=True)
            with open(file_path, "a+") as log_file:
                print(f'{datetime.now()}:\t{message}', file = log_file)
        except Exception as exeption:
            print(exeption)
            
    def get_short_log_file_path():
        current_time = datetime.now()
        return f"{logger.short_log_folder_path}/starpacker_log_{current_time.year}{current_time.month}{current_time.day}.log"
    
    def get_debug_log_file_path():
        current_time = datetime.now()
        return f"{logger.debug_log_folder_path}/starpacker_debug_log_{current_time.year}{current_time.month}{current_time.day}.log"
    
    def set_log_config(logs_config):
        logger.console_logging_enabled = logs_config["console_logging_enabled"]
        logger.file_logging_enabled = logs_config["file_logging_enabled"]
        logger.debug_logging_enabled = logs_config["debug_logging_enabled"]
        logger.short_logging_enabled = logs_config["short_logging_enabled"]
        logger.debug_log_folder_path = logs_config["debug_log_folder_path"]
        logger.short_log_folder_path = logs_config["short_log_folder_path"]
