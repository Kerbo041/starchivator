from struct import pack, unpack
from model.TDateTime import TDateTime


def x_dat_file_write(
    x_dat_path, array_of_buffer_values, header_text, special_buffer_signal, next_parameter_index
):
    with open(x_dat_path, "wb") as x_file:
        header_write(x_file, header_text, special_buffer_signal, next_parameter_index)
        write_buffered_values(x_file, array_of_buffer_values)


def header_write(
    file, header_text: str, special_buffer_signal: int, next_parameter_index: int
):
    file.write(header_text.encode())
    file.write(pack("<d", TDateTime.datetime_to_tdatetime()))
    file.write(pack("<i", special_buffer_signal))
    file.write(pack("<i", next_parameter_index))


def write_buffered_values(file, array_of_buffer_values):
    for number in array_of_buffer_values:
        file.write(pack("<i", array_of_buffer_values[number]["Number"]))
        file.write(array_of_buffer_values[number]["Value"])
        file.write(array_of_buffer_values[number]["Signal"])
