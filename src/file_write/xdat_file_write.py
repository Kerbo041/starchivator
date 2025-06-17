from struct import pack, unpack
from model.TDateTime import TDateTime
from datetime import datetime
import os
from model.BufferArray import BufferArray
from model.TechnologicalParameter import TechnologicalParameter
from model.Logger import Logger
from model.Config import Config


def x_dat_file_write(
    buffer_parameters_array: BufferArray,
    config: Config,
    logger: Logger,
):
    try:
        directory_path = os.path.dirname(config.file_paths.path_x_dat)
        if not os.path.exists(directory_path):
            os.makedirs(directory_path, exist_ok=True)
            
        with open(config.file_paths.path_x_dat, "wb+") as x_file:
            header_write(
                x_file,
                config.header_texts.x_dat,
                buffer_parameters_array.buffer_number,
                buffer_parameters_array.buffer_length,
                logger,
            )
            write_buffered_values(x_file, buffer_parameters_array.buffer_array, logger)
            
        logger.log(
            f"{config.file_paths.path_x_dat}\t file written, current size is {buffer_parameters_array.buffer_length}, current sync value is {buffer_parameters_array.buffer_number}",
            debug=True,
        )

    except Exception as exception:
        logger.log(f"error:\tx.dat writing:\t{exception}")


def header_write(
    file,
    header_text: str,
    special_buffer_signal: int,
    next_parameter_index: int,
    logger: Logger,
):
    try:
        file.seek(0)
        file.write(header_text.encode())
        file.write(pack("<d", TDateTime.datetime_to_tdatetime(datetime.now())))
        file.write(pack("<i", special_buffer_signal))
        file.write(pack("<i", next_parameter_index))
    except Exception as exception:
        logger.log(f"error:\tx.dat header writing:\t{exception}")


def write_buffered_values(file, buffered_parameters_array, logger: Logger):
    try:
        for parameter in buffered_parameters_array:
            if type(parameter) == TechnologicalParameter:
                file.write(pack("<i", parameter.get_number()))
                file.write(parameter.get_value())
                file.write(parameter.get_signal())
    except Exception as exception:
        logger.log(f"error:\tx.dat values writing:\t{exception}")
