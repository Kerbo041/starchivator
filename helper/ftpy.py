from datetime import datetime, timedelta
import struct
import random
import time
import shutil


def datetime_to_tdatetime_in_bytes(time_in_datetime: datetime) -> bytes:
    delta_time = time_in_datetime - datetime(1899, 12, 30)
    tdatetime = delta_time.total_seconds() / 3600 / 24
    return struct.pack("<d", tdatetime)

def get_values_from_line(str):
    out = []
    for value in str.split(";"):
        try:
            int_val = int(value)
        except:
            int_val = 0
        out.append(int_val)
    return out

def get_random_value(start, end):
    if end > 2000000000:
        end = 2000000000
    return int(round(random.random() * end + start))

def make_out0(db_path, out_path):
    db_file = open(db_path, "r")
    out_file = open(out_path, "wb")
    db_raw_data = [get_values_from_line(line) for line in db_file.readlines()]
    now = datetime_to_tdatetime_in_bytes(datetime.now())
    for line in db_raw_data:
        # number = struct.pack("<i", int(line[0]))
        number = line[0].to_bytes(4, byteorder="little")
        value = get_random_value(line[2], line[3])
        byte_value = struct.pack("<i", value)
        signal = b"\x03"
        out_file.write(number)
        out_file.write(now)
        out_file.write(byte_value)
        out_file.write(signal)
    db_file.close()
    out_file.close()


def make_out1(db_path, out_path):
    db_file = open(db_path, "r")
    out_file = open(out_path, "bw")
    db_raw_data = [
        get_values_from_line(line) for line in db_file.readlines()
    ]
    now = datetime_to_tdatetime_in_bytes(datetime.now())
    for line in db_raw_data:
        number = struct.pack("<i", line[0])
        value = struct.pack("<i", random.randint(0, line[1]))
        signal = b"\x05"
        out_file.write(number)
        out_file.write(now)
        out_file.write(value)
        out_file.write(signal)
    db_file.close()
    out_file.close()


def main():
    dba_path = "files/DB_A.CSV"
    dbd_path = "files/DB_D.CSV"
    # out0_path = "files/created/out.0"
    # out1_path = "files/created/out.1"
    out0_path = "C:/spd3/out/out.0"
    out1_path = "C:/spd3/out/out.1"

    while True:
        make_out0(dba_path, out0_path)
        make_out1(dbd_path, out1_path)
        now = str(datetime.now()).replace(".", ",").replace(":", "-")
        print(now)
        # shutil.copy(out0_path, f"files/outfiles/{now}_0")
        # shutil.copy(out1_path, f"files/outfiles/{now}_1")
        time.sleep(1)


main()
