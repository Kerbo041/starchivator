from datetime import datetime
from file_write.outdat_file_write import out_dat_file_write
from file_write.xdat_file_write import x_dat_file_write
from file_write.archive_file_write import archive_file_write
from data_check.check_data import compare_buffer_and_write_data_array
from file_read.out_file_read_buffered import get_out_data_with_buffer
from model.Logger import Logger
from model.TechnologicalParametersArray import TechnologicalParametersArray
from model.BufferArray import BufferArray
from model.Config import Config


def do_archiving_iteration(
    current_parameters_array: TechnologicalParametersArray,
    reading_parameters_array: TechnologicalParametersArray,
    buffer_parameters_array: BufferArray,
    config: Config,
    logger: Logger,
):

    get_out_data_with_buffer(config, reading_parameters_array, logger)

    compare_buffer_and_write_data_array(
        current_parameters_array,
        reading_parameters_array,
        buffer_parameters_array,
        config,
        logger,
    )

    x_dat_file_write(buffer_parameters_array, config, logger)
    
    out_dat_file_write(
        current_parameters_array, buffer_parameters_array.buffer_number, config, logger
    )

    archive_file_write(
        current_parameters_array, buffer_parameters_array, config, logger
    )

    logger.log("one archivation iteration done")


def start(config_path="src/config.json"):
    config = Config(config_path)
    logger = Logger(config.log_config)
    current_parameters_array = TechnologicalParametersArray(
        total_number_of_parameters=config.program_parameters.total_number_of_values
    )
    reading_parameters_array = TechnologicalParametersArray(
        total_number_of_parameters=config.program_parameters.total_number_of_values
    )
    buffer_parameters_array = BufferArray(
        config.program_parameters.buffer_size, datetime(1, 1, 1)
    )

    while True:
        do_archiving_iteration(
            current_parameters_array,
            reading_parameters_array,
            buffer_parameters_array,
            config,
            logger,
        )


start()
