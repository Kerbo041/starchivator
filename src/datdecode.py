from typing import BinaryIO
from TDateTime import *

# from __future__ import annotations
from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import BinaryIO
import struct

read_path = "files/20240617.VO3"


def read_file(path: str) -> []:
    with open(path, "rb") as file:
        return bytearray(file.read())


if __name__ == "__main__":

    file = read_file(read_path)

    file_start = [
        [f"{i+j}: {hex(file[i+j])} \t" for j in range(16)] for i in range(0, 128, 16)
    ]
    fole = open("by.txt", "w")
    for line in file_start:
        for point in line:
            print(point, end="", file=fole)
        print("", file=fole)
    fole.close()
    progname = file[0:16].decode("utf-8")
    print(progname)

    date = TDateTime.tdatetime_to_datetime(file[16:24])
    print(date)

    points = [struct.unpack("<i", file[i : i + 4 :]) for i in range(24, 119, 4)]
    size1 = struct.unpack("<i", file[119:123])
    size2 = struct.unpack("<i", file[123:127])
    print(size1)
    print(size2)

    datafile = open("dataV03.txt", "w")
    print(progname, file=datafile)
    print(date, file=datafile)
    print(date, file=datafile)
    print(size1, file=datafile)
    print(size2, file=datafile)

    # file_data = [
    #     f"status: {file[i]}, data = {file[i + 1]} {file[i + 2]} {file[i + 3]} {file[i + 4]}"
    #     for i in range(128, len(file), 5)
    # ]
    file_data = []
    for i in range(127, len(file), 5):
        line = f"status:\t{hex(file[i])}\t data: \t{hex(file[i + 1])}\t{hex(file[i + 2])}\t{hex(file[i + 3])}\t{hex(file[i + 4])}"
        file_data.append(line)
    for line in file_data:
            print(line, file=datafile)
    datafile.close()
