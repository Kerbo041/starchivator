from datetime import datetime, timedelta
from json import load
from file_write.outdat_file_write import out_dat_file_write
from file_write.xdat_file_write import x_dat_file_write
from file_write.archive_file_write import archive_file_write
from data_check.check_data import check_data_array
from data_check.data_change import data_change
from data_check.buffer_data_to_array import buffer_data
from file_read.out_file_read_buffered import get_out_data_with_buffer
from model.Logger import Logger
from model.TechnologicalParametersArray import TechnologicalParametersArray
from model.TechnologicalParameter import TechnologicalParameter
from model.BufferArray import BufferArray
from model.Config import Config
import os

def do_archivation_iteration(
    current_parameters_array: TechnologicalParametersArray,
    array_of_buffered_parameters: BufferArray,
    config: Config,
    logger:Logger
):
    current_time = current_parameters_array.get_time()

    new_current_time = datetime.now()

    if current_time.hour != new_current_time.hour:
        is_new_hour = True
    else:
        is_new_hour = False
    if current_time.day != new_current_time.day:
        is_new_day = True
        max_archive_file_age = 7
        for archive_file_name in os.listdir(config.file_paths.path_arc_folder):
            try:
                archive_file_date = datetime.strptime(archive_file_name, "%Y%m%d.VO3")
                archive_file_timedelta = (datetime.now() - archive_file_date)/timedelta(days=1)
                if archive_file_timedelta > max_archive_file_age:
                    os.remove(os.path.join(config.file_paths.path_arc_folder, archive_file_name))
            except Exception as e:
                print(e)
    else:
        is_new_day = False

    readed_data = get_out_data_with_buffer(config)
    
    if readed_data == None:
        Logger.log(
            f"{config.file_paths.path_out_0}, {config.file_paths.path_out_1}: error with reading"
        )
        return (
            current_parameters_array,
            array_of_buffered_parameters,
        )

    total_number_of_values = 0
    for number in current_values:
        if readed_data[number]["Status"] == True:
            total_number_of_values += 1
    if old_total_number_of_values > total_number_of_values:
        old_total_number_of_values = total_number_of_values
        logger.log(
            f"{file_paths["Path_out_0"]}, {file_paths["Path_out_1"]}: error with number of params"
        )
        return (
            current_values,
            array_of_buffered_parameters,
            current_time,
            special_buffer_signal,
            current_parameter_index,
            old_total_number_of_values,
        )
    old_total_number_of_values = total_number_of_values

    logger.log(
        f"{file_paths["Path_out_0"]} and {file_paths["Path_out_1"]} parsed", debug=True
    )

    changed_values = check_data_array(current_values, readed_data)

    array_of_buffered_parameters, current_parameter_index, special_buffer_signal = (
        buffer_data(
            array_of_buffered_parameters,
            changed_values,
            current_parameter_index,
            special_buffer_signal,
        )
    )

    # current_values = readed_new_data
    data_change(current_values, readed_data)

    x_dat_file_write(
        file_paths["Path_x_dat"],
        array_of_buffered_parameters,
        headers["XDat"],
        special_buffer_signal,
        current_parameter_index,
    )
    # print(f"current_values_length is {len(current_values)}")
    out_dat_file_write(
        file_paths["Path_out_dat"],
        current_values,
        headers["OutDat"],
        special_buffer_signal,
        values_count=200000,
    )

    archive_file_write(
        file_paths["Path_arc_folder"],
        headers["Archive"],
        current_values,
        changed_values,
        current_time,
        is_new_hour,
        is_new_day,
        BLOCK_NUMBER,
    )
    total_number_of_values = 0
    for number in current_values:
        if current_values[number]["Status"] == True:
            total_number_of_values += 1
    if len(changed_values) > 0:
        logger.log(f"changed: {len(changed_values)}, total: {total_number_of_values}")
    logger.log("one archivation iteration done")
    return (
        current_values,
        array_of_buffered_parameters,
        current_time,
        special_buffer_signal,
        current_parameter_index,
        old_total_number_of_values,
    )


def start(config_path="src/config.json", header_text="StarPack____"):
    BLOCK_NUMBER = 3
    config = load(open(config_path, "r"))
    file_paths = config["Paths"]
    headers = config["HeaderTexts"]
    log_config = config["Logs"]
    current_time = datetime(1, 1, 1)
    special_buffer_signal = 0
    current_parameter_index = 0
    current_values = {
        i: {
            "Value": b"\xff\xff\xff\xff",
            "Signal": b"\xff",
            "Status": False,
        }
        for i in range(200000)
    }
    logger.set_log_config(log_config)
    logger.set_default_log_folder_path(__file__)
    array_of_buffered_parameters = {}
    old_total_number_of_values = 0
    while True:
        (
            current_values,
            array_of_buffered_parameters,
            current_time,
            special_buffer_signal,
            current_parameter_index,
            old_total_number_of_values,
        ) = do_archivation_iteration(
            current_values,
            array_of_buffered_parameters,
            current_time,
            special_buffer_signal,
            current_parameter_index,
            file_paths,
            headers,
            BLOCK_NUMBER,
            old_total_number_of_values,
        )


start()
