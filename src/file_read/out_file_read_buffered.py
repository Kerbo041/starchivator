from struct import pack, unpack
from datetime import datetime
from model.logger import logger
from model.technological_parameter import technological_parameter
from shutil import copy2
import os
def parse_readed_out_file_from_buffer(out_file_buffered_data, number_of_values, out_file_path):
    try:
        out_file_data = {}
        for iter in range(number_of_values):
            out_file_line = out_file_buffered_data[iter * 17 : (iter + 1) * 17]
            readed_data = read_out_file_line_from_buffer(out_file_line)
            if readed_data == None:
                continue
            out_file_data[readed_data["Number"]] = {
                "Value": readed_data["Value"],
                "Signal": readed_data["Signal"],
                "Status": readed_data["Status"],
            }
        logger.log("readed {len(out_file_data)} from {out_file_path}", debug= True)
        return out_file_data
    except Exception as exception:
        logger.log("error: parsing {out_file_path}: {exception}")
        return None


def read_out_file_line_from_buffer(out_file_line):
    if len(out_file_line) < 17:
        return None
    number_in_bytes = out_file_line[0:4]
    if number_in_bytes == b"":
        return None
    number = unpack("<i", number_in_bytes)[0]
    if number == -1:
        return None
    date = out_file_line[4:12]
    value = out_file_line[12:16]
    signal = out_file_line[16:17]
    status = True
    # if date == b"\xff\xff\xff\xff\xff\xff\xff\xff" or number_in_bytes == b"\xff\xff\xff\xff":
    #     status = False
    return {
        "Number": number,
        "Date": date,
        "Value": value,
        "Signal": signal,
        "Status": status,
    }


def get_empty_line():
    return {
        "Number": -1,
        "NumberInBytes": b"\xff\xff\xff\xff",
        "Date": b"\xff\xff\xff\xff\xff\xff\xff\xff",
        "Value": b"\xff\xff\xff\xff",
        "Signal": b"\xff",
        "Status": False,
    }


def fill_values_end_with_empty_lines(values, count_of_values):
    try:
        new_values = {}
        for i in range(count_of_values):
            if i in values.keys():
                new_values[i] = values[i]
            else:
                new_values[i] = get_empty_line()
        return new_values
    except Exception as exception:
        logger.log("error: {exception}")
        return None


# def fill_values_end_with_empty_lines(values, count_of_values):
#     new_values = values
#     for i in range(count_of_values):
#         if not i in new_values.keys():
#             new_values[i] = get_empty_line()
#     return new_values


def arrays_join(out_0_file_data, out_1_file_data, analog_count=20000):
    try:
        out_values = {}
        for analog_value_key in out_0_file_data:
            out_values[analog_value_key] = out_0_file_data[analog_value_key]
        for discrete_value_key in out_1_file_data:
            out_values[analog_count + discrete_value_key] = out_1_file_data[
                discrete_value_key
            ]
        return out_values
    except Exception as exception:
        logger.log("error: {exception}")
        return None

def get_out_data_with_buffer(
    out_0_path, out_1_path, default_out_0_path, default_out_1_path, analog_count=20000, discrete_count=180000, copy_file = False
):
    try:
        if copy_file:
            directory_path = os.path.dirname(default_out_0_path)
            if not os.path.exists(directory_path):
                os.makedirs(directory_path, exist_ok=True)
            directory_path = os.path.dirname(default_out_1_path)
            if not os.path.exists(directory_path):
                os.makedirs(directory_path, exist_ok=True)
            copy2(out_0_path, default_out_0_path)
            copy2(out_1_path, default_out_1_path)
            with open(default_out_0_path, mode="rb") as out_file:
                buffered_out_0_file_data = out_file.read()
            with open(default_out_1_path, mode="rb") as out_file:
                buffered_out_1_file_data = out_file.read()
        else:
            with open(out_0_path, mode="rb") as out_file:
                buffered_out_0_file_data = out_file.read()
            with open(out_1_path, mode="rb") as out_file:
                buffered_out_1_file_data = out_file.read()

    except Exception as exeption:
        logger.debug_log("file reading: {exeption}")
        return None

    out_0_file_data = parse_readed_out_file_from_buffer(
        buffered_out_0_file_data, analog_count, out_0_path
    )
    out_1_file_data = parse_readed_out_file_from_buffer(
        buffered_out_1_file_data, discrete_count, out_1_path
    )
    
    if out_0_file_data == None or out_1_file_data == None:
        return None
    
    out_0_file_data = fill_values_end_with_empty_lines(out_0_file_data, analog_count)
    out_1_file_data = fill_values_end_with_empty_lines(out_1_file_data, discrete_count)

    if out_0_file_data == None or out_1_file_data == None:
        return None
    
    out_values = arrays_join(out_0_file_data, out_1_file_data, analog_count)
    
    if out_values == None:
        return None

    return out_values


