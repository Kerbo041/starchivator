from struct import pack, unpack
from src.model.TDateTime import TDateTime

def get_x_dat_header(header_text: str, time: TDateTime, buffer_signal: int, number_of_changed_values: int):
    





def get_outdat_header(header_text: str, time: TDateTime, buffer_signal: int):
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
    header = get_outdat_header(out_dat_path, writing_time, buffer_signal)
    main_part = outdat_main_part_set(writing_values)
    with open(out_dat_path, "wb") as dat_file:
        dat_file.write(header)
        dat_file.write(main_part)

def file_starter(path):
    with open(path, "wb") as fout:
        fout.write(pack("<i", 0))
        fout.write(pack("<i", 0))
        fout.write(b"\xaa\xbb\xcc\xdd\xee\xff")
        for i in range(20):
            fout.write(b"\x00\x00\x00\x00\x00\x00\x00\x00")
            # fout.write(pack("<i", randint(0, 2000000)))


def write_changed_values(path, values):
    print("dowriting")
    with open(path, "rb+") as file:
        start_count = get_count_of_values(file)
        # values = [pack("<i", randint(0,2000000)) for i in range(15)]
        # print(values)
        breaked = False
        i = 0
        for value in values:
            if get_count_of_values(file) >= 20:
                restart_file(file)
                breaked = True
                break
            place_value(file, value, start_count + i)
            set_count_of_values(file, get_count_of_values(file) + 1)
            i += 1
    return breaked



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
