from struct import pack, unpack
from src.model.TDateTime import TDateTime


class DatFile():
    
    def __init__(self, file_path: str, header_text: str, special_buffer_signal: int= 0):
        self.file_path = file_path
        self.file = None
        self.is_file_opened = False
        self.header_text = header_text
        self.special_buffer_signal = special_buffer_signal
        
    def open_file(self):
        try:
            self.file = open(self.file_path, "wb")
            self.is_file_opened = True
            
        except Exception as e:
            self.file = None
            self.is_file_opened = False
    
    def close_file(self):
        if self.file and self.is_file_opened:
            self.file.close()
            self.is_file_opened = False
    
    def check_file(self):
        if self.file and self.is_file_opened:
            return self.file
    
    def set_header(self):
        self.header = self.header_text.encode()
        self.header += TDateTime.datetime_to_tdatetime()
        self.header += pack("<i", self.special_buffer_signal)
        
    def get_header(self):
        return self.header
    
    def write_value_to_file(self):
        self.set_header()
        with open(self.file_path, "wb") as out_file:
            out_file.write(self.get_header())
            for value in self.values:
                out_file.write(value["ValueInBytes"])
                out_file.write(value["SignalInBytes"])
    
    