from struct import pack, unpack
import model.TDateTime

class OutFile():
    
    def __init__(out_file_path):
        with open(out_file_path, "rb") as out_file:
            pass
            
class OutFileRecord():
    
    def __init__(self, record_in_bytes):
        self.name = unpack("<i", record_in_bytes[0:4:])
        self.date = TDateTime.tdatetime_to_datetime(unpack("<d", record_in_bytes[0:4:]))
        self.value = unpack("<i", record_in_bytes[0:4:])
        self.signal = unpack("<c", record_in_bytes[0:4:])