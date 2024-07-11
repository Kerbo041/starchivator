from typing import BinaryIO
from TDateTime import *

# from __future__ import annotations
from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import BinaryIO
import struct

read_path = "files/out.dat"


def read_file(path: str) -> []:
    with open(path, "rb") as file:
        return bytearray(file.read())


if __name__ == "__main__":

    file = read_file(read_path)

    progname = file[0:16].decode("utf-8")
    print(progname)

    date = TDateTime.tdatetime_to_datetime(file[16:24])
    print(date)



    datafile = open("datfiile.txt", "w")
    print(progname, file=datafile)
    print(date, file=datafile)

    # file_data = [
    #     f"status: {file[i]}, data = {file[i + 1]} {file[i + 2]} {file[i + 3]} {file[i + 4]}"
    #     for i in range(128, len(file), 5)
    # ]
    file_data = []
    for i in range(27, len(file)-1, 5):
        line = f"status:\t{hex(file[i])}\t data: \t{hex(file[i + 1])}\t{hex(file[i + 2])}\t{hex(file[i + 3])}\t{hex(file[i + 4])}"
        file_data.append(line)
    for line in file_data:
            print(line, file=datafile)
    datafile.close()
