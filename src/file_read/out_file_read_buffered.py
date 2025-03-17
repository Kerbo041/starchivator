from struct import pack, unpack
from datetime import datetime
# import mmap
from model.logger import logger
from model.TechnologicalParameter import technological_parameter

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
        logger.log(f"readed {len(out_file_data)} from {out_file_path}", debug= True)
        return out_file_data
    except Exception as exception:
        logger.log(f"error: parsing {out_file_path}: {exception}")
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
        logger.log(f"error: {exception}")
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
        logger.log(f"error: {exception}")
        return None

def get_out_data_with_buffer(
    out_0_path, out_1_path, analog_count=20000, discrete_count=180000
):
    try:
        time1 = datetime.now()
        with open(out_0_path, mode="rb") as out_file:
            buffered_out_0_file_data = out_file.read()
            # with mmap.mmap(
            #     out_file.fileno(), length=0, access=mmap.ACCESS_READ
            # ) as out_file_mapped:
            #     buffered_out_0_file_data = out_file_mapped.read()
        time2 = datetime.now()
        # logger.debug_log(f"{out_0_path} was readed successfully, reading time is {time2-time1}")
        with open(out_1_path, mode="rb") as out_file:
            buffered_out_1_file_data = out_file.read()
            # with mmap.mmap(
            #     out_file.fileno(), length=0, access=mmap.ACCESS_READ
            # ) as out_file_mapped:
            #     buffered_out_1_file_data = out_file_mapped.read()
        time3 = datetime.now()
        # logger.log(f"{out_1_path} was readed successfully, reading time is {time3-time2}", debug = True)
    except Exception as exeption:
        logger.debug_log(f"file reading: {exeption}")
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


