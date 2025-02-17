from datetime import datetime
import os

class logger():
    
    console_logging_enabled = True
    file_logging_enabled = True
    log_folder_path = "logs/"
    def __init__(self):
        pass
    
    def logging(self, message):
        if type(message) is not str:
            message = str(message)
        if self.console_logging_enabled:
            self.console_logging(message)
        if self.file_logging_enabled:
            self.file_logging(message)
    
    def console_logging(self, message):
        print(f'{datetime.now()}:\t{message}')
        
    def file_logging(self, message):
        try:
            if not os.path.exists(self.log_folder_path):
                os.mkdir(self.log_folder_path, parents=True, exist_ok=True)
            with open(self.get_log_file_path(), "wb") as log_file:
                print(f'{datetime.now()}:\t{message}', file = log_file)
        except Exception as exeption:
            print(exeption)
            
    def get_log_file_path(self):
        current_time = datetime.now()
        return f"{self.log_folder_path}/{current_time.year}{current_time.month}{current_time.day}.log"