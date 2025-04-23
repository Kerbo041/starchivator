import os
from struct import pack, unpack
from model.TDateTime import TDateTime
from datetime import datetime
from model.Logger import Logger
from model.TechnologicalParameter import TechnologicalParameter
from model.TechnologicalParametersArray import TechnologicalParametersArray
from model.Config import Config


def out_dat_file_write(
    config: Config,
    parameters_array_object: TechnologicalParametersArray,
    special_buffer_signal,
    logger: Logger,
):
    try:
        directory_path = os.path.dirname(config.file_paths.path_out_dat)
        if not os.path.exists(directory_path):
            os.makedirs(directory_path, exist_ok=True)
        with open(config.file_paths.path_out_dat, "wb") as out_dat_file:
            header_write(
                out_dat_file,
                config.file_paths.path_out_dat,
                config.header_texts.out_dat,
                special_buffer_signal,
                logger
            )
            write_all_data_to_out_dat(out_dat_file, parameters_array_object, logger)
            logger.log(
                f"{config.file_paths.path_out_dat}\twritten, current sync value is {special_buffer_signal}",
                debug=True,
            )
    except Exception as exception:
        logger.log(f"error:\tout.dat writing:\t{exception}")


def header_write(
    file, out_dat_path, header_text, special_buffer_signal, logger: Logger
):
    try:
        file.write(header_text.encode())
        file.write(pack("<d", TDateTime.datetime_to_tdatetime(datetime.now())))
        file.write(pack("<i", special_buffer_signal))
        logger.log(f"{out_dat_path}\tfile header written", debug=True)
    except Exception as exception:
        logger.log(f"error:\tout.dat header writing:\t{exception}")


def write_all_data_to_out_dat(
    out_dat_file, parameters_array_object: TechnologicalParametersArray, logger:Logger
):
    try:
        for parameter in parameters_array_object.parameters_array:
            if type(parameter) == TechnologicalParameter:
                out_dat_file.write(parameter.get_value())
                out_dat_file.write(parameter.get_state())
        # logger.log("{out_dat_path}\tfile written", debug = True)
    except Exception as exception:
        logger.log(f"error:\tout.dat header writing:\t{exception}")
