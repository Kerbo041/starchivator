from struct import pack, unpack
from model.TDateTime import TDateTime


def x_dat_file_write(
    x_dat_path, changed_values, header_text, special_buffer_signal, next_parameter_index
):
    with open(x_dat_path, "ab+") as x_file:
        header_write(x_file, header_text, special_buffer_signal, next_parameter_index)
        is_writing_breaked = write_changed_values(x_file, changed_values)
    return is_writing_breaked


def header_write(
    file, header_text: str, special_buffer_signal: int, next_parameter_index: int
):
    file.write(header_text.encode())
    file.write(pack("<d", TDateTime.datetime_to_tdatetime()))
    file.write(pack("<i", special_buffer_signal))
    file.write(pack("<i", next_parameter_index))


def write_changed_values(file, сhanged_values):
    is_writing_breaked = False
    for key in сhanged_values:
        writing_index = get_index(file)
        if writing_index >= 7279:
            is_writing_breaked = True
            set_index(file, 0)
            break
        place_value(file, key, сhanged_values[key], writing_index)
        writing_index += 1
        set_index(file, writing_index)
        if writing_index >= 7279:
            is_writing_breaked = True
            set_index(file, 0)
            special_buffer_signal_set(file, (special_buffer_signal_get(file) + 1))
            break
        else:
            set_index(file, writing_index)
    return is_writing_breaked


def place_value(file, number, value, count):
    index = count * 9 + 32
    file.seek(index)
    file.write(pack("<i", number))
    file.write(value["Value"])
    file.write(value["Signal"])


def special_buffer_signal_set(file, counter):
    file.seek(24)
    file.write(pack("<i", counter))


def special_buffer_signal_get(file):
    file.seek(24)
    old_iter = unpack("<i", file.read(4))[0]
    return old_iter


def get_index(file):
    file.seek(28)
    return unpack("<i", file.read(4))[0]


def set_index(file, value):
    file.seek(28)
    file.write(pack("<i", value))
