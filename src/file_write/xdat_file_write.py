from struct import pack, unpack
from model.TDateTime import TDateTime
from datetime import datetime
import os
from model.Logger import Logger

def x_dat_file_write(
    x_dat_path, array_of_buffer_values, header_text, special_buffer_signal, next_parameter_index
):
    try:
        directory_path = os.path.dirname(x_dat_path)
        if not os.path.exists(directory_path):
            os.makedirs(directory_path, exist_ok=True)
        with open(x_dat_path, "wb") as x_file:
            header_write(x_file, header_text, special_buffer_signal, next_parameter_index)
            write_buffered_values(x_file, array_of_buffer_values)
        # logger.debug_log(f"{x_dat_path} written, current size is {next_parameter_index}, current sync value is {special_buffer_signal}")
        
        Logger.log(f"{x_dat_path}\t file written, current size is {next_parameter_index}, current sync value is {special_buffer_signal}", debug = True)

    except Exception as exception:
        Logger.log(f"error:\tx.dat writing:\t{exception}")

def header_write(
    file, header_text: str, special_buffer_signal: int, next_parameter_index: int
):
    try:
        file.write(header_text.encode())
        file.write(pack("<d", TDateTime.datetime_to_tdatetime(datetime.now())))
        file.write(pack("<i", special_buffer_signal))
        file.write(pack("<i", next_parameter_index))
    except Exception as exception:
        Logger.log(f"error:\tx.dat header writing:\t{exception}")


def write_buffered_values(file, array_of_buffer_values):
    try:
        for number in array_of_buffer_values:
            file.write(pack("<i", array_of_buffer_values[number]["Number"]))
            file.write(array_of_buffer_values[number]["Value"])
            file.write(array_of_buffer_values[number]["Signal"])
    except Exception as exception:
        Logger.log(f"error:\tx.dat values writing:\t{exception}")

