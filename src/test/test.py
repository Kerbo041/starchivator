# from struct import pack, unpack
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

a = bytearray(b'\x70\xaa\x17\x00\xc0\xd6\xe5\x00')
b = hex(a[0]).replace("0x", "")
print(type(b))
c = str(b)
print(type(c))
print(c)

for i in b:
    print(i)

print(f"{a}\t{b}\t{c}")