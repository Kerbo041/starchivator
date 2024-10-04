from struct import pack, unpack
from model.TDateTime import TDateTime

# from src.model.TDateTime import TDateTime

def out_dat_file_write(out_dat_path, all_values, header_text, special_buffer_signal, values_count=200000):
    with open(out_dat_path, "wb") as dat_file:
        header_write(dat_file, header_text, special_buffer_signal)
        write_all_data_to_out_dat(dat_file, all_values, values_count=200000)


def header_write(file, header_text, special_buffer_signal):
    file.write(header_text.encode())
    file.write(pack("<d", TDateTime.datetime_to_tdatetime()))
    file.write(pack("<i", special_buffer_signal))


# def write_all_data_to_out_dat(file, all_values, values_count=200000):
#     for value in all_values:
#         file.write(all_values[value]["Value"])
#         file.write(all_values[value]["Signal"])

def write_all_data_to_out_dat(file, all_values, values_count=200000):
    for i in range(values_count):
        file.write(all_values[i]["Value"])
        file.write(all_values[i]["Signal"])