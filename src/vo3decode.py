from __future__ import annotations
from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import BinaryIO
import struct

# read_path = "files/20240617.VO3"
read_path = "files/20220614.VO2"
desc_path = "decoded_files/dataV02.txt"


def tdatetime_to_datetime(tdatetime_in_bytes: bytes) -> datetime:
    tdatetime = struct.unpack('<d', tdatetime_in_bytes)[0]
    return datetime(1899, 12, 30) + timedelta(days=tdatetime)


def read_blocks(file, array_size = 500000):
    blocks= []

    while True:
        block = read_block(file, array_size)
        if block is None:
            break
        blocks.append(block)
    return blocks


def read_block(file, array_size):
    array_type = 1
    timestamp = 8

    new_portion_of_data = file.read(array_type)
    if new_portion_of_data == b'':
        return None
    creation_time = tdatetime_to_datetime(file.read(timestamp))
    block_data = []
    byte_of_the_array_type = int.from_bytes(new_portion_of_data, 'little')

    if byte_of_the_array_type == 0:
        for i in range(1, array_size + 1, 5):
            block_data.append({
                "data": file.read(4),
                "status": file.read(1)
            })

    elif byte_of_the_array_type == 1:
        array_size = int.from_bytes(file.read(4), "little") * 9
        for i in range(1, array_size + 1, 9):
            block_data.append({
                "address" : file.read(4), 
                "data": file.read(4), 
                "status": file.read(1)
            })
    else:
        print('Неверный формат файла')
        exit(1)
    return {
        "type": byte_of_the_array_type,
        "creation_time": creation_time,
        "data": block_data
    }

if __name__ == "__main__":

    file = open(read_path, "rb")

    progname = file.read(16).decode("utf-8")
    date = tdatetime_to_datetime(file.read(8))
    points = [struct.unpack("<l", file.read(4)) for i in range(24, 119, 4)]
    parameters_photo_size = struct.unpack("<i", file.read(4))[0]
    changed_parameters_array_size = struct.unpack("<i", file.read(4))[0]


    datafile = open(desc_path, "w")
    print(progname, file=datafile)
    print(date, file=datafile)
    print(parameters_photo_size, file=datafile)
    print(changed_parameters_array_size, file=datafile)

    blocks = read_blocks(file, parameters_photo_size)
    for block in blocks:
        if block["type"] == 0:
            print("photo of parameters", file=datafile)
        elif block["type"] == 1:
            print("array of changed parameters", file=datafile)
        print(f"creation time: {block["creation_time"]}", file=datafile)
        for value in block["data"]:
            for key in value:
                print(f"{key}:\t", end="", file=datafile)
                for i in value[key]:
                    print(f"{hex(i)} ", end="", file=datafile)
                print("\t", end="", file=datafile)
            print("", file=datafile)
    
    datafile.close()
