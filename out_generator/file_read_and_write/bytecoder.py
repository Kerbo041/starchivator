import struct
import misc
from datetime import datetime, timedelta
def datetime_to_tdatetime_in_bytes(time_in_datetime: datetime) -> bytes:
    delta_time = time_in_datetime - datetime(1899, 12, 30)
    tdatetime = delta_time.total_seconds() / 3600 / 24
    return struct.pack("<d", tdatetime)

def bytecoder(values):
    output_file_data_in_bytes = []
    for line in values:
        byte_line = b""
        number_in_bytes = line["number"].to_bytes(4, byteorder="little")
        time_in_bytes = datetime_to_tdatetime_in_bytes(line["time"])
        value_in_bytes = struct.pack("<f", line["value"])
        signal_in_bytes = line["signal"]

        byte_line += number_in_bytes
        byte_line += time_in_bytes
        byte_line += value_in_bytes
        byte_line += signal_in_bytes
        
        output_file_data_in_bytes.append(byte_line)

    return output_file_data_in_bytes
