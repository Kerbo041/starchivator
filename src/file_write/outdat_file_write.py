from struct import pack, unpack
from src.model.TDateTime import TDateTime


def outdat_header_set(header_text: str, time: TDateTime, buffer_signal: int):
    header = b""
    for symbol in header_text:
        header += pack("<c", symbol)
    header += pack("<d", time.get_tdatetime)
    header += pack("<i", buffer_signal)
    return header


def outdat_main_part_set(array_of_values):
    main_part = b""
    for value in array_of_values:
        main_part += value["Value"]
        main_part += value["Signal"]


def out_dat_file_write(out_dat_path, writing_values, writing_time, buffer_signal):
    header = outdat_header_set(out_dat_path, writing_time, buffer_signal)
    main_part = outdat_main_part_set(writing_values)
    with open(out_dat_path, "wb") as dat_file:
        dat_file.write(header)
        dat_file.write(main_part)


def header_count_add(file):
    file.seek(0)
    old_iter = unpack("<i", file.read(4))[0]
    new_iter = old_iter + 1
    file.seek(0)
    file.write(pack("<i", new_iter))


def header_count_set(file, counter):
    file.seek(0)
    file.write(pack("<i", counter))


def header_count_check(file):
    file.seek(0)
    old_iter = unpack("<i", file.read(4))[0]
    return old_iter


def place_value(file, value, count):
    count = count * 8 + 14
    file.seek(count)
    file.write(pack("<i", value["Number"]))
    file.write(value["Value"])


def get_count_of_values(file):
    file.seek(4)
    return unpack("<i", file.read(4))[0]


def set_count_of_values(file, value):
    file.seek(4)
    file.write(pack("<i", value))


def restart_file(file):
    set_count_of_values(file, 0)
    header_count_add(file)


def write_all_data_to_out_dat(path, values, count):
    print("\nwriting all")
    for value in values:
        print(value["Value"], end="")
    with open(path, "wb") as file:
        file.write(pack("<i", count))
        file.write(b"\xaa\xbb\xcc\xdd\xee\xff")
        for value in values:
            file.write(value["Value"])
