from struct import pack, unpack


def read_out_file(out_file_path, number_of_values=0):
    with open(out_file_path) as out_file:
        iter = 0
        reading = True
        out_file_data = []
        while iter < number_of_values or reading:
            read_buffer = read_out_file_line(out_file)
            line = read_buffer[0]
            reading = read_buffer[1]
            if reading:
                out_file_data.append(line)
            iter += 1
    return out_file_data


def read_out_file_line(out_file):
    try:
        number = out_file.read(4)
        date = out_file.read(8)
        value = out_file.read(4)
        signal = out_file.read(4)
        return (
            {
                "Number": unpack("<i", number),
                "Date": date,
                "Value": value,
                "Signal": signal,
            },
            True,
        )
    except:
        return (None, False)


def get_empty_line(number):
    return (
        {
            "Number": number,
            "Date": b"\x00\x00\x00\x00\x00\x00\x00\x00",
            "Value": b"\xff\xff\xff\xff",
            "Signal": b"\x08",
        },
    )


def fill_values_end_with_empty_lines(values, count):
    analog_length = len(values)
    if analog_length < 20000:
        for i in range(analog_length, count):
            values[i] = get_empty_line(i)


def arrays_join(out_0_file_data, out_1_file_data, analog_count=20000):
    out_values = []
    for analog_value in out_0_file_data:
        out_values.append(analog_value)
    for discrete_value in out_1_file_data:
        discrete_value["Number"] = discrete_value["Number"] + analog_count
        out_values.append(discrete_value)
    return out_values


def get_out_data(out_0_path, out_1_path, analog_count=20000, discrete_count=180000):
    out_0_file_data = read_out_file(out_0_path)
    out_1_file_data = read_out_file(out_1_path)

    out_0_file_data = fill_values_end_with_empty_lines(out_0_file_data, analog_count)
    out_1_file_data = fill_values_end_with_empty_lines(out_1_file_data, discrete_count)

    out_values = arrays_join(out_0_file_data, out_1_file_data, analog_count)
