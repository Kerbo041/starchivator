from struct import unpack
from datetime import datetime, timedelta

def decode_int_bytes(entered_string):
    data = bytes.fromhex(entered_string.replace(" ", ""))
    return unpack("<i", data)

# def show_int():
#     label_int["text"] = decode_int_bytes(entry_int.get())     # получаем введенный текст

# def decode_date_bytes(entered_string):
#     return tdatetime_to_datetime(bytes.fromhex(entered_string.replace(" ", "")))

# def tdatetime_to_datetime(tdatetime_in_bytes: bytes) -> datetime:
#     tdatetime = unpack("<d", tdatetime_in_bytes)[0]
#     return datetime(1899, 12, 30) + timedelta(days=tdatetime)

# def show_date():
#     label_date["text"] = decode_date_bytes(entry_data.get())     # получаем введенный текст
    
def decode():
    pass