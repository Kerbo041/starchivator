from struct import pack, unpack


def read_out_file(out_file_path, number_of_values=0):
    try:
        with open(out_file_path) as out_file:
            out_file_data = {}
            for iter in range(number_of_values):
                out_file_data[iter] = read_out_file_line(out_file)
        return out_file_data
    except:
        return {
            iter: get_empty_line() for iter in range(number_of_values)
        }


def read_out_file_line(out_file):
    try:
        number_in_bytes = out_file.read(4)
        number = unpack("<i", number_in_bytes)
        date = out_file.read(8)
        value = out_file.read(4)
        signal = out_file.read(1)

        if number == -1:
            status = False
        else:
            status = True

        return (
            {
                "Number": number,
                "Date": date,
                "Value": value,
                "Signal": signal,
                "Status": status,
            },
            True,
        )
    except:
        return get_empty_line()


def get_empty_line():
    return (
        {
            "Number": -1,
            "NumberInBytes": b"\xff\xff\xff\xff",
            "Date": b"\x00\x00\x00\x00\x00\x00\x00\x00",
            "Value": b"\x00\x00\x00\x00",
            "Signal": b"\x08",
            "Status": False,
        },
    )


def fill_values_end_with_empty_lines(values, count):
    data_length = len(values)
    if data_length < count:
        for i in range(data_length, count):
            if not i in values.keys():
                values[i] = get_empty_line()


def arrays_join(out_0_file_data, out_1_file_data, analog_count=20000):
    out_values = []
    for analog_value_key in out_0_file_data:
        out_values.append(out_0_file_data[analog_value_key])
    for discrete_value_key in out_1_file_data:
        out_values.append(out_1_file_data[discrete_value_key + analog_count])
    return out_values


def get_out_data(out_0_path, out_1_path, analog_count=20000, discrete_count=180000):

    out_0_file_data = read_out_file(out_0_path)
    out_1_file_data = read_out_file(out_1_path)

    out_0_file_data = fill_values_end_with_empty_lines(out_0_file_data, analog_count)
    out_1_file_data = fill_values_end_with_empty_lines(out_1_file_data, discrete_count)

    out_values = arrays_join(out_0_file_data, out_1_file_data, analog_count)

    return out_values
