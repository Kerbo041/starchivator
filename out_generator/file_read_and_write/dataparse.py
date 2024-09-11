import asyncio
import time
import misc.misc as misc
import struct
def reader_db_a(db_path):
    db_file = open(db_path, "r")
    db_values = []
    for line in db_file.readlines():
        line_splited = line.split(";")
        db_values.append(
            {
                "number": int(line_splited[0]),
                "min": float(line_splited[2]),
                "max": float(line_splited[3]),
            }
        )
    return db_values


def reader_db_d(db_path):
    fin = open(db_path, "r")
    db_values = []
    for line in fin.readlines():
        line_splited = line.split(";")
        db_values.append(
            {
                "number": int(line_splited[0]), 
                "length": int(line_splited[1])}
        )
    return db_values

def get_data_from_out_dat_file(read_path):

    dat_file = open(read_path, "rb")

    program_name = dat_file.read(16).decode("utf-8")
    date = misc.tdatetime_to_datetime(dat_file.read(8))
    reserv = dat_file.read(4)
    blocks = []
    while True:
        block = dat_file.read(5)
        if len(block) < 5:
            break
        blocks.append(block)
    dat_file.close()
    return blocks

    

    size_of_photo = int(len(file_data) / 5)

    return {
        "program_name": program_name,
        "date": date,
        "size_of_photo": size_of_photo,
        "file_data": file_data,
    }

def get_data_from_x_dat_file(read_path):
    dat_file = open(read_path, "rb")

    program_name = dat_file.read(16).decode("utf-8")
    date = misc.tdatetime_to_datetime(dat_file.read(8))
    index = dat_file.read(4)
    start = dat_file.read(4)
    blocks = []
    while True:
        block = dat_file.read(9)
        if len(block) < 9:
            break
        blocks.append(read_block(block))
    dat_file.close()
    return {
        "date": date,
        "index": index,
        "start": start,
        "blocks": blocks
    }

def read_block(block):
    return {
        "number": struct.unpack("<i", block[0:4:]),
        "value" : struct.unpack("<i", block[4:8:]),
        "signal": block[8]
    }