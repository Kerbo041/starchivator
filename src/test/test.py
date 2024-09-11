from struct import pack, unpack

# from datetime import datetime, timedelta
# import time

# def tdatetime_to_datetime(tdatetime_in_bytes: bytes) -> datetime:
#     tdatetime = unpack('<d', tdatetime_in_bytes)[0]
#     return datetime(1899, 12, 30) + timedelta(days=tdatetime)

# zero = datetime(1899, 12, 30)
# bb = b'\x70\xaa\x17\x00\xc0\xd6\xe5\x40'
# #2022-06-14 00:00:00.975000
# #\x70\xaa\x17\x00\xc0\xd6\xe5\x40
# days = unpack("<d", bb)

# #now = datetime.now()
# now = tdatetime_to_datetime(bb)
# print(now)
# print(zero)
# delta =  (now - zero).total_seconds()/3600/24
# baray = (bytearray(pack("<d", delta)))
# for bar in baray:
#     print(hex(bar), end=" - ")

# def datetime_to_tdatetime(time_in_datetime: datetime) -> bytes:
#     delta_time =  time_in_datetime - datetime(1899, 12, 30)
#     tdatetime = delta_time.total_seconds()/3600/24
#     return  pack("<d", tdatetime)

# #40 42 0f 20 a0 86 01 20 20 1f d5 12 9f 2f 36 e6 40 20 20
# #20 20 20 20 0a 4e 37 53 1e 01 20 20 20 20 20 20 08 01 20 20 20 52 56 37 53 df 02 20 20 20 20 80 3f 30 02 20 20 20 52 56 37 53 df

# a = bytearray(b'\x70\xaa\x17\x00\xc0\xd6\xe5\x00')
# b = hex(a[0]).replace("0x", "")
# print(type(b))
# c = str(b)
# print(type(c))
# print(c)

# for i in b:
#     print(i)

# print(f"{a}\t{b}\t{c}")

# a = bytearray(b'\x40\x0d\x03\x20')
# b = bytearray(b'\x20\x4e\x00\x00')
# print(unpack("<i", a))
# print(unpack("<i", b))

# a = bytearray(b'\x40\x42\x0f\x20')
# b = bytearray(b'\xa0\x86\x01\x20')
# print(unpack("<i", a))
# print(unpack("<i", b))
# c2 b9 01 20


# from datetime import datetime, timedelta

# def tdatetime_to_datetime(tdatetime_in_bytes: bytes) -> datetime:
#     tdatetime = unpack("<d", tdatetime_in_bytes)[0]
#     return datetime(1899, 12, 30) + timedelta(days=tdatetime)

# print(tdatetime_to_datetime(b'\x57\x56\x37\x53\x06\x01\x00\x00'))
# print(unpack("<d", b'\x57\x56\x37\x53\x06\x01\x00\x00'))
def get_str_from_byte(byte_value):
    raw_str = str(hex(byte_value))[2:4:]
    if len(raw_str)== 1:
        raw_str = "0" + raw_str
    return raw_str

# print("--------------------------------")
# a = b'\xaa\x50\x07\xf6\x03'
# for i in a:
#     print(get_str_from_byte(i))

# print(b"\xff"*17)



# from random import randint

# a = [randint(1, 50) for i in range(10)]
# b = 255
# with open("writing_test.txt", "wb") as f:
#     for i in a:
#         f.write(i.to_bytes(4, byteorder="little"))
# with open("writing_test.txt", "rb+") as f:
#     f.seek(3)
#     f.write(b.to_bytes(4, byteorder="little"))
# print(a)
# for i in a:
#     print(i.to_bytes(4, byteorder="little"))
# print(f"- {b.to_bytes(4, byteorder="little")}")


hex_string = "0x"+ ("11"*4)

an_integer = int(hex_string, 16)

hex_value = hex(an_integer)

print(bytearray(an_integer.to_bytes(4,byteorder="little")))