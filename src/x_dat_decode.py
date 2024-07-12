from __future__ import annotations
from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import BinaryIO
import struct

read_path = "files/x.dat"
desc_path = "decoded_files/xdat_decoded.txt"

def tdatetime_to_datetime(tdatetime_in_bytes: bytes) -> datetime:
    tdatetime = struct.unpack('<d', tdatetime_in_bytes)[0]
    return datetime(1899, 12, 30) + timedelta(days=tdatetime)





def read_data(file):
    
    line_data = []
    while True:
        new_portion_of_data = file.read(9)
        if new_portion_of_data == b'':
            break
        line = {
            "address" : file.read(4), 
            "data": file.read(4), 
            "status": file.read(1)
        }
        for key in line:
            print(f"{key}:\t", end="")
            for i in line[key]:
                print(f"{hex(i)} ", end="")
            print("\t", end="")
        print("")
        line_data.append(line)
    return line_data

if __name__ == "__main__":

    file = open(read_path, "rb")

    progname = file.read(16).decode("utf-8")
    date = tdatetime_to_datetime(file.read(8))
    special_index = struct.unpack("<i", file.read(4))[0]
    start_index = struct.unpack("<i", file.read(4))[0]


    datafile = open(desc_path, "w")
    print(progname, file=datafile)
    print(date, file=datafile)


    data = read_data(file)
    for line_data in data:
        for key in line_data:
            print(f"{key}:\t", end="", file=datafile)
            for i in line_data[key]:
                print(f"{hex(i)} ", end="", file=datafile)
            print("\t", end="", file=datafile)
        print("", file=datafile)
    
    datafile.close()
