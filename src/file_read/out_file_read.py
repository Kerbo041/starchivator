from struct import pack, unpack
from datetime import datetime
from model.logger import logger

def read_out_file(out_file_path, number_of_values=0):
    try:
        with open(out_file_path, "rb") as out_file:
            out_file_data = {}
            for iter in range(number_of_values):
                readed_data = read_out_file_line(out_file)
                if readed_data == None:
                    continue
                out_file_data[readed_data["Number"]] = {
                    "Value": readed_data["Value"],
                    "Signal": readed_data["Signal"],
                }
        return out_file_data
    except Exception as exeption:
        logger.debug_log(exeption)
        return {iter: get_empty_line() for iter in range(number_of_values)}


def read_out_file_line(out_file):
    try:
        number_in_bytes = out_file.read(4)
        if number_in_bytes == b"":
            return None
        number = unpack("<i", number_in_bytes)[0]
        if number == -1:
            return None
        date = out_file.read(8)
        value = out_file.read(4)
        signal = out_file.read(1)
        return {"Number": number, "Date": date, "Value": value, "Signal": signal}
    except Exception as exeption:
        logger.debug_log(exeption)
        return get_empty_line()


def get_empty_line():
    return {
            # "Number": -1,
            # "NumberInBytes": b"\xff\xff\xff\xff",
            # "Date": b"\x00\x00\x00\x00\x00\x00\x00\x00",
            "Value": b"\xff\xff\xff\xff",
            "Signal": b"\xff",
        }


def fill_values_end_with_empty_lines(values, count_of_values):
    new_values = {}
    for i in range(count_of_values):
        if i in values.keys():
            new_values[i] = values[i]
        else:
            new_values[i] = get_empty_line()
    return new_values


# def fill_values_end_with_empty_lines(values, count_of_values):
#     new_values = values
#     for i in range(count_of_values):
#         if not i in new_values.keys():
#             new_values[i] = get_empty_line()
#     return new_values


def arrays_join(out_0_file_data, out_1_file_data, analog_count=20000):
    out_values = {}
    for analog_value_key in out_0_file_data:
        out_values[analog_value_key] = out_0_file_data[analog_value_key]
    for discrete_value_key in out_1_file_data:
        out_values[analog_count + discrete_value_key] = out_1_file_data[
            discrete_value_key
        ]
    return out_values


def get_out_data(out_0_path, out_1_path, analog_count=20000, discrete_count=180000):
    time1 = datetime.now()
    out_0_file_data = read_out_file(out_0_path, analog_count)
    time2 = datetime.now()
    out_1_file_data = read_out_file(out_1_path, discrete_count)
    time3 = datetime.now()
    # print("writing time analog is {time2 - time1}")
    # print("since {time1}")
    # print("to {time2}")
    # print("writing time discrete is {time3 - time2}")
    # print("since {time2}")
    # print("to {time3}")
    # print("out0 file len is {len(out_0_file_data)}")
    # print("out1 file len is {len(out_1_file_data)}")
    
    out_0_file_data = fill_values_end_with_empty_lines(out_0_file_data, analog_count)
    out_1_file_data = fill_values_end_with_empty_lines(out_1_file_data, discrete_count)

    out_values = arrays_join(out_0_file_data, out_1_file_data, analog_count)

    return out_values

