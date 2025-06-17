from struct import pack, unpack
from datetime import datetime
from model.Logger import Logger
from model.TechnologicalParameter import TechnologicalParameter
from model.TechnologicalParametersArray import TechnologicalParametersArray
from model.Config import Config, ConfigFilePaths


def parse_readed_out_file_from_buffer(
    out_file_buffered_data,
    reading_buffer_array: TechnologicalParametersArray,
    number_of_values,
    logger: Logger,
):
    try:
        for iter in range(number_of_values):
            out_file_line = out_file_buffered_data[iter * 17 : (iter + 1) * 17]
            if len(out_file_line) < 17:
                return None
            number_in_bytes = out_file_line[0:4]
            if number_in_bytes == b"":
                return None
            number = unpack("<i", number_in_bytes)[0]
            reading_buffer_array.parameters_array[iter].set_all_values(
                number, out_file_line[4:12], out_file_line[12:16], out_file_line[16:17]
            )
        reading_buffer_array.set_time()

    except Exception as exception:
        logger.log(f"error: parsing: {exception}")
        return None


def fill_values_end_with_empty_lines(array_of_values, count_of_values):
    len_of_array = len(array_of_values)
    if len_of_array < (count_of_values * 17):
        for i in range(len_of_array, (count_of_values * 17)):
            array_of_values += b"\xff"


def arrays_join(out_0_file_data, out_1_file_data, config: Config, logger: Logger):
    try:
        if out_0_file_data == None or out_1_file_data == None:
            return None
        fill_values_end_with_empty_lines(
            out_0_file_data, config.TOTAL_NUMBER_OF_ANALOG_VALUES
        )
        fill_values_end_with_empty_lines(
            out_1_file_data, config.TOTAL_NUMBER_OF_DISCRETE_VALUES
        )
        out_values = out_0_file_data + out_1_file_data
        return out_values
    except Exception as exception:
        logger.log(f"error: {exception}")
        return None


def get_out_data_with_buffer(
    config: Config, reading_buffer_array: TechnologicalParametersArray, logger: Logger
) -> TechnologicalParametersArray:
    try:

        with open(config.file_paths.path_out_0, mode="rb") as out_file:
            buffered_out_0_file_data = bytearray(out_file.read())

        with open(config.file_paths.path_out_1, mode="rb") as out_file:
            buffered_out_1_file_data = bytearray(out_file.read()) 

    except Exception as exeption:
        logger.debug_log(f"file reading: {exeption}")
        return None
    out_file_buffered_data = arrays_join(
        buffered_out_0_file_data,
        buffered_out_1_file_data,
        config,
        logger
    )
    if out_file_buffered_data == None:
        return None

    parse_readed_out_file_from_buffer(
        out_file_buffered_data,
        reading_buffer_array,
        config.TOTAL_NUMBER_OF_VALUES,
        logger,
    )
    logger.log(
        f"{config.file_paths.path_out_0} and {config.file_paths.path_out_1} parsed", debug=True
    )
