from struct import pack, unpack
from model.TDateTime import TDateTime
from datetime import datetime
from model.logger import logger


# from src.model.TDateTime import TDateTime
import os
from shutil import copy2

def out_dat_file_write(
    out_dat_path, default_out_dat_path, all_values, header_text, special_buffer_signal, values_count=200000, copy_file = False, remove_file = False
):
    try:
        directory_path = os.path.dirname(out_dat_path)
        if not os.path.exists(directory_path):
            os.makedirs(directory_path, exist_ok=True)
        if copy_file:
            default_directory_path = os.path.dirname(default_out_dat_path)
            if not os.path.exists(default_directory_path):
                os.makedirs(directory_path, exist_ok=True)
            with open(default_out_dat_path, "rb+") as dat_file:
                header_write(dat_file, default_out_dat_path, header_text, special_buffer_signal)
                write_all_data_to_out_dat(dat_file, all_values, values_count, default_out_dat_path)
                if remove_file:
                    try:
                        os.remove(out_dat_path)
                    except:
                        pass
                copy2(default_out_dat_path, out_dat_path)
        else:
            with open(out_dat_path, "rb+") as dat_file:
                header_write(dat_file, out_dat_path, header_text, special_buffer_signal)
                write_all_data_to_out_dat(dat_file, all_values, values_count, out_dat_path)
        logger.log(
                f"{out_dat_path}\twritten, current sync value is {special_buffer_signal}", debug = True
            )
            # logger.log("")
    except Exception as exception:
        logger.log(f"error:\tout.dat writing:\t{exception}")



def header_write(file, out_dat_path, header_text, special_buffer_signal):
    try:
        file.seek(0)
        file.write(header_text.encode())
        file.write(pack("<d", TDateTime.datetime_to_tdatetime(datetime.now())))
        file.write(pack("<i", special_buffer_signal))
        logger.log(f"{out_dat_path}\tfile header written", debug = True)
    except Exception as exception:
        logger.log(f"error:\tout.dat header writing:\t{exception}")



def write_all_data_to_out_dat(file, all_values, values_count, out_dat_path):
    try:
        file.seek(28)
        for i in range(values_count):
            file.write(all_values[i]["Value"])
            file.write(all_values[i]["Signal"])
        # logger.log("{out_dat_path}\tfile written", debug = True)
    except Exception as exception:
        logger.log(f"error:\tout.dat header writing:\t{exception}")

