from datetime import datetime, timedelta
import struct


def tdatetime_to_datetime(tdatetime_in_bytes: bytes) -> datetime:
    tdatetime = struct.unpack("<d", tdatetime_in_bytes)[0]
    return datetime(1899, 12, 30) + timedelta(days=tdatetime)


def datetime_to_tdatetime_in_bytes(time_in_datetime: datetime) -> bytes:
    delta_time = time_in_datetime - datetime(1899, 12, 30)
    tdatetime = delta_time.total_seconds() / 3600 / 24
    return struct.pack("<d", tdatetime)


def get_str_from_byte(byte_value):
    raw_str = str(hex(byte_value))[2:4:]
    if len(raw_str) == 1:
        raw_str = "0" + raw_str
    return raw_str


def print_byte_line(byte_line, file_to_write):
    for byte_value in byte_line:
        print(get_str_from_byte(byte_value), file=file_to_write, end="")
        print(" ", file=file_to_write, end="")
