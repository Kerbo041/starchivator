from __future__ import annotations
from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import BinaryIO
import struct

read_path = "src/files/out.dat"
desc_path = "src/decoded_files/encoded.txt"

def tdatetime_to_datetime(tdatetime_in_bytes: bytes) -> datetime:
    tdatetime = struct.unpack('<d', tdatetime_in_bytes)[0]
    return datetime(1899, 12, 30) + timedelta(days=tdatetime)


def datetime_to_tdatetime_in_bytes(time_in_datetime: datetime) -> bytes:
        delta_time =  time_in_datetime - datetime(1899, 12, 30)
        tdatetime = delta_time.total_seconds()/3600/24
        return struct.pack("<d", tdatetime)


def aaa():

    dat_file = open(read_path, "rb")

    program_name = dat_file.read(16).decode("utf-8")
    date = tdatetime_to_datetime(dat_file.read(8))
    
    vo3_file = open(desc_path, "wb")
    

    file_data = dat_file.read()
    size_of_photo = int(len(file_data)/5)
    vo3_file.write(program_name.encode("utf-8"))
    vo3_file.write(datetime_to_tdatetime_in_bytes(date))

    address_array = [b"\xff\xff\xff\xff" for i in range(24)]
    address_array[date.hour] = b"\x80\x00\x00\x00"
    for value in address_array:
        vo3_file.write(value)
    vo3_file.write(struct.pack("<i",size_of_photo))
    vo3_file.write(struct.pack("<i",int(size_of_photo/10)))
    vo3_file.write(file_data)
if __name__ == "__main__":
    aaa()