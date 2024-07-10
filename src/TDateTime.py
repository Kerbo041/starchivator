from datetime import datetime, timedelta

import struct

class TDateTime:
    
    def __init__(self) -> None:
        pass
    
    def tdatetime_to_datetime(count_days_in_byte: bytes) -> datetime:
        count_days_in_float = struct.unpack('<d', count_days_in_byte)[0]
        return datetime(1899, 12, 30) + timedelta(days=count_days_in_float)
