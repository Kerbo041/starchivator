from struct import pack, unpack
from datetime import datetime
from model.Logger import Logger
from model.TechnologicalParameter import TechnologicalParameter
from model.TechnologicalParametersArray import TechnologicalParametersArray
from model.Config import Config, ConfigFilePaths


def parse_readed_out_file_from_buffer(
    out_file_buffered_data, number_of_values, out_file_path, logger: Logger
):
    try:
        out_file_data_parameters_array = []
        for iter in range(number_of_values):
            out_file_line = out_file_buffered_data[iter * 17 : (iter + 1) * 17]
            readed_parameter = read_out_file_line_from_buffer(out_file_line)
            if readed_parameter == None:
                continue
            out_file_data_parameters_array.append(readed_parameter)
        logger.log(
            f"readed {len(out_file_data_parameters_array)} from {out_file_path}",
            debug=True,
        )
        return out_file_data_parameters_array
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
    return TechnologicalParameter(
        number, out_file_line[4:12], out_file_line[12:16], out_file_line[16:17]
    )


def fill_values_end_with_empty_lines(array_of_values, count_of_values):
    last_element_index = len(array_of_values)
    if last_element_index < count_of_values:
        for i in range(last_element_index, count_of_values):
            array_of_values.append(TechnologicalParameter())


def arrays_join(out_0_file_data, out_1_file_data, analog_count, logger: Logger):
    try:
        out_values = []
        for analog_value in out_0_file_data:
            out_values.append(analog_value)
        for discrete_value_key in out_1_file_data:
            out_values[analog_count + discrete_value_key] = out_1_file_data[
                discrete_value_key
            ]
        return out_values
    except Exception as exception:
        logger.log(f"error: {exception}")
        return None


def get_out_data_with_buffer(config: Config, logger:Logger) -> TechnologicalParametersArray:
    try:

        with open(config.file_paths.path_out_0, mode="rb") as out_file:
            buffered_out_0_file_data = out_file.read()

        with open(config.file_paths.path_out_1, mode="rb") as out_file:
            buffered_out_1_file_data = out_file.read()

    except Exception as exeption:
        logger.debug_log(f"file reading: {exeption}")
        return None

    out_0_file_data = parse_readed_out_file_from_buffer(
        buffered_out_0_file_data,
        config.TOTAL_NUMBER_OF_ANALOG_VALUES,
        config.file_paths.path_out_0,
    )
    out_1_file_data = parse_readed_out_file_from_buffer(
        buffered_out_1_file_data,
        config.TOTAL_NUMBER_OF_DISCRETE_VALUES,
        config.file_paths.path_out_1,
    )

    if out_0_file_data == None or out_1_file_data == None:
        return None

    out_values = arrays_join(
        out_0_file_data, out_1_file_data, config.TOTAL_NUMBER_OF_ANALOG_VALUES
    )

    if out_values == None:
        return None

    return TechnologicalParametersArray(out_values, config.TOTAL_NUMBER_OF_VALUES)
