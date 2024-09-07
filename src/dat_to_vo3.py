from datetime import datetime, timedelta
import struct

read_path = "src/files/out.dat"
desc_path = "src/decoded_files/encoded.txt"


def tdatetime_to_datetime(tdatetime_in_bytes: bytes) -> datetime:
    tdatetime = struct.unpack("<d", tdatetime_in_bytes)[0]
    return datetime(1899, 12, 30) + timedelta(days=tdatetime)


def datetime_to_tdatetime_in_bytes(time_in_datetime: datetime) -> bytes:
    delta_time = time_in_datetime - datetime(1899, 12, 30)
    tdatetime = delta_time.total_seconds() / 3600 / 24
    return struct.pack("<d", tdatetime)


def get_data_from_dat_file(read_path):

    dat_file = open(read_path, "rb")

    program_name = dat_file.read(16).decode("utf-8")
    date = tdatetime_to_datetime(dat_file.read(8))
    file_data = dat_file.read()

    dat_file.close()

    size_of_photo = int(len(file_data) / 5)

    return {
        "program_name": program_name,
        "date": date,
        "size_of_photo": size_of_photo,
        "file_data": file_data,
    }


def write_data_to_archive_file(desc_path, data_to_archive):
    program_name = data_to_archive["program_name"]
    date = data_to_archive["date"]
    size_of_photo = data_to_archive["size_of_photo"]
    file_data = data_to_archive["file_data"]

    vo3_file = open(desc_path, "wb")
    vo3_file.write(program_name.encode("utf-8"))
    vo3_file.write(datetime_to_tdatetime_in_bytes(date))

    address_array = [b"\xff\xff\xff\xff" for i in range(24)]
    address_array[date.hour] = b"\x80\x00\x00\x00"
    for value in address_array:
        vo3_file.write(value)
    vo3_file.write(struct.pack("<i", size_of_photo))
    vo3_file.write(struct.pack("<i", int(size_of_photo / 10)))
    vo3_file.write(file_data)
    vo3_file.close()


if __name__ == "__main__":
    data_to_archive = get_data_from_dat_file(read_path)
    write_data_to_archive_file(desc_path, data_to_archive)
