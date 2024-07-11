from __future__ import annotations
from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import BinaryIO
import struct

read_path = "files/20240617.VO3"
desc_path = "decoded_files/"

def read_file(path: str) -> bytearray:
    with open(path, "rb") as file:
        return bytearray(file.read())



def tdatetime_to_datetime(tdatetime_in_bytes: bytes) -> datetime:
    tdatetime = struct.unpack('<d', tdatetime_in_bytes)[0]
    return datetime(1899, 12, 30) + timedelta(days=tdatetime)


if __name__ == "__main__":

    file = read_file(read_path)

    progname = file[0:16].decode("utf-8")
    date = tdatetime_to_datetime(file[16:24])
    points = [struct.unpack("<l", file[i : i + 4 :]) for i in range(24, 119, 4)]
    parameters_photo_size = struct.unpack("<i", file[119:123])[0]
    changed_parameters_array_size = struct.unpack("<i", file[123:127])[0]


    datafile = open(desc_path + "dataV03.txt", "w")
    print(progname, file=datafile)
    print(date, file=datafile)
    print(parameters_photo_size, file=datafile)
    print(changed_parameters_array_size, file=datafile)

    file_data = []
    for i in range(127, len(file), 5):
        line = f"status:\t{hex(file[i])}\t data: \t{hex(file[i + 1])}\t{hex(file[i + 2])}\t{hex(file[i + 3])}\t{hex(file[i + 4])}"
        file_data.append(line)
    for line in file_data:
            print(line, file=datafile)
    datafile.close()
