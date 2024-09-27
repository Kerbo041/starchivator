from struct import pack, unpack
from src.model.TDateTime import TDateTime

class OutDatFile():
    
    def __init__(self, file_path: str, header_text: str, special_buffer_signal: int, values: dict):
        self.file_path = file_path
        self.header_text = header_text
        self.special_buffer_signal = special_buffer_signal
        self.values = values
        
    def set_header(self):
        self.header = self.header_text.encode()
        self.header += TDateTime.datetime_to_tdatetime()
        self.header += pack("<i", self.special_buffer_signal)
        
    def get_header(self):
        return self.header
    
    
    def write_to_file(self):
        self.set_header()
        with open(self.file_path, "wb") as out_file:
            out_file.write(self.get_header())
            for value in self.values:
                out_file.write(value["ValueInBytes"])
                out_file.write(value["SignalInBytes"])
        