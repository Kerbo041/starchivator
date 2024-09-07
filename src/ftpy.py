from datetime import datetime, timedelta
import struct
import random
import time
import shutil
def datetime_to_tdatetime_in_bytes(time_in_datetime: datetime) -> bytes:
    delta_time = time_in_datetime - datetime(1899, 12, 30)
    tdatetime = delta_time.total_seconds() / 3600 / 24
    return struct.pack("<d", tdatetime)


def make_out0(db_path, out_path):
    db_file = open(db_path, "r")
    out_file = open(out_path, "bw")
    db_raw_data = [line.split(";") for line in db_file.readlines()]
    now = datetime_to_tdatetime_in_bytes(datetime.now())
    for line in db_raw_data:
        number = struct.pack("<i", int(line[0]))
        number = int(line[0]).to_bytes(length=4,byteorder="little")
        value = struct.pack("<i", random.randint(int(line[1]), int(line[2])))
        signal = b"\x05"
        print(number, file = out_file, end = "")
        print(now, file = out_file, end = "")
        print(value, file = out_file, end = "")
        print(signal, file = out_file, end = "")
    db_file.close()
    out_file.close()


def make_out1(db_path, out_path):
    db_file = open(db_path, "r")
    out_file = open(out_path, "bw")
    db_raw_data = [[int(value) for value in line.split(";")] for line in db_file.readlines()]
    now = datetime_to_tdatetime_in_bytes(datetime.now())
    for line in db_raw_data:
        number = struct.pack("<i", line[0])
        value = struct.pack("<i", random.randint(0, line[1]))
        signal = b"\x05"
        print(number, file = out_file, end = "")
        print(now, file = out_file, end = "")
        print(value, file = out_file, end = "")
        print(signal, file = out_file, end = "")
    db_file.close()
    out_file.close()


def main():
    dba_path = "DB_A.CSV"
    dbd_path = "DB_D.CSV"
    out0_path = "out.0"
    out1_path = "out.1"

    while True:
        make_out0(dba_path, out0_path)
        make_out1(dbd_path, out1_path)
        now = str(datetime.now()).replace(".", ",").replace(":", "-")
        print(now)
        shutil.copy(out0_path, f"outfiles/{now}_0")
        shutil.copy(out1_path, f"outfiles/{now}_1")
        time.sleep(1)

main()
