from datetime import datetime, timedelta
from struct import pack, unpack

class TDateTime:
    def __init__(self, time_in_datetime: datetime = None, tdatetime_in_bytes: bytes = None) -> None:
        if tdatetime_in_bytes:
            self.time = self.tdatetime_in_bytes_to_datetime(tdatetime_in_bytes)
        elif time_in_datetime:
            self.time = time_in_datetime
        else:
            self.time = datetime.now()
    
    def tdatetime_to_datetime(tdatetime: float) -> datetime:
        return datetime(1899, 12, 30) + timedelta(days=tdatetime)
    
    def tdatetime_in_bytes_to_datetime(tdatetime_in_bytes: bytes) -> datetime:
        tdatetime = unpack('<d', tdatetime_in_bytes)[0]
        return datetime(1899, 12, 30) + timedelta(days=tdatetime)
    

    def datetime_to_tdatetime(time_in_datetime: datetime) -> bytes:
        delta_time =  time_in_datetime - datetime(1899, 12, 30)
        tdatetime = delta_time.total_seconds()/3600/24
        return  tdatetime
    
    def datetime_to_tdatetime_in_bytes(time_in_datetime: datetime) -> bytes:
        delta_time =  time_in_datetime - datetime(1899, 12, 30)
        tdatetime = delta_time.total_seconds()/3600/24
        return  pack("<d", tdatetime)
    
    def __str__(self) -> str:
        return str(self.time)
    
    
    
    
now = TDateTime(tdatetime_in_bytes = b'\x70\xaa\x17\x00\xc0\xd6\xe5\x40')

print(now)
