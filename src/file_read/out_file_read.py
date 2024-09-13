def read_out_file(out_file_path, number_of_values = 0):
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
            {"Number": number, "Date": date, "Value": value, "Signal": signal},
            True,
        )
    except:
        return ({"Number": None, "Date": None, "Value": None, "Signal": None}, False)
