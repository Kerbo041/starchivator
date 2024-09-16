from struct import pack
from src.model.TDateTime import TDateTime


def outdat_header_set(header_text: str, time: TDateTime, buffer_signal: int):
    header = b""
    for symbol in header_text:
        header += pack("<c", symbol)
    header += pack("<d", time.get_tdatetime)
    header += pack("<i", buffer_signal)
    return header


def outdat_main_part_set(array_of_values):
    main_part = b""
    for value in array_of_values:
        main_part += value["Value"]
        main_part += value["Signal"]


def out_dat_file_write(out_dat_path, writing_values, writing_time, buffer_signal):
    header = outdat_header_set(out_dat_path, writing_time, buffer_signal)
    main_part = outdat_main_part_set(writing_values)
    with open(out_dat_path, "wb") as dat_file:
        dat_file.write(header)
        dat_file.write(main_part)
