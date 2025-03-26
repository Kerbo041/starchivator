# from src.file_write.outdat_file_write import out_dat_file_write
# from src.file_write.xdat_file_write import write_changed_values
# from src.data_check.check_data import check_data_array
# from src.file_read.out_file_read import read_out_file
# from src.config.config import get_config
from file_write.outdat_file_write import out_dat_file_write
from file_write.xdat_file_write import x_dat_file_write
from file_write.archive_file_write import archive_file_write
from data_check.check_data import check_data_array
from data_check.data_change import data_change
from data_check.buffer_data_to_array import buffer_data
from file_read.out_file_read import get_out_data
from file_read.out_file_read_buffered import get_out_data_with_buffer
from datetime import datetime
from json import load
from model.logger import logger
import os
import time


def do_archivation_iteration(
    current_values,
    array_of_buffered_parameters,
    current_time,
    special_buffer_signal,
    current_parameter_index,
    file_paths,
    headers,
    BLOCK_NUMBER,
    old_total_number_of_values,
):
    
    
    copy_files = True
    remove_files = True
    
    
    new_current_time = datetime.now()
    if current_time.hour != new_current_time.hour:
        is_new_hour = True
    else:
        is_new_hour = False
    if current_time.day != new_current_time.day:
        is_new_day = True
    else:
        is_new_day = False
    current_time = new_current_time

    readed_new_data = get_out_data_with_buffer(
        file_paths["Path_out_0"],
        file_paths["Path_out_1"],
        file_paths["DefaultPath_out_0"],
        file_paths["DefaultPath_out_1"],
        analog_count=20000,
        discrete_count=180000,
        copy_file=copy_files
    )
    if readed_new_data == None:
        logger.log(
            f"{file_paths["Path_out_0"]}, {file_paths["Path_out_1"]}: error with reading"
        )
        return (
            current_values,
            array_of_buffered_parameters,
            current_time,
            special_buffer_signal,
            current_parameter_index,
            old_total_number_of_values,
        )

    total_number_of_values = 0
    for number in current_values:
        if readed_new_data[number]["Status"] == True:
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

    changed_values = check_data_array(current_values, readed_new_data)

    array_of_buffered_parameters, current_parameter_index, special_buffer_signal = (
        buffer_data(
            array_of_buffered_parameters,
            changed_values,
            current_parameter_index,
            special_buffer_signal,
        )
    )


    # current_values = readed_new_data
    data_change(current_values, readed_new_data)

    x_dat_file_write(
        file_paths["Path_x_dat"],
        file_paths["DefaultPath_x_dat"],
        array_of_buffered_parameters,
        headers["XDat"],
        special_buffer_signal,
        current_parameter_index,
        copy_file=copy_files,
        remove_file= remove_files
    )
    # print(f"current_values_length is {len(current_values)}")
    out_dat_file_write(
        file_paths["Path_out_dat"],
        file_paths["DefaultPath_out_dat"],
        current_values,
        headers["OutDat"],
        special_buffer_signal,
        values_count=200000,
        copy_file=copy_files,
        remove_file= remove_files
    )

    archive_file_write(
        file_paths["Path_arc_folder"],
        file_paths["DefaultPath_arc_folder"],
        headers["Archive"],
        current_values,
        changed_values,
        current_time,
        is_new_hour,
        is_new_day,
        BLOCK_NUMBER,
        copy_file=copy_files
    )
    total_number_of_values = 0
    for number in current_values:
        if current_values[number]["Status"] == True:
            total_number_of_values += 1
    if len(changed_values) > 0:
        logger.log(f"changed: {len(changed_values)}, total: {total_number_of_values}")
    logger.log("one archivation iteration done")
    time.sleep(0.5)
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
    # script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_dir = os.path.join(script_dir, "files\\")
    file_paths = config["Paths"]
    file_paths["DefaultPath_out_dat"] = os.path.join(file_dir, "out.dat")
    file_paths["DefaultPath_x_dat"] = os.path.join(file_dir, "x.dat")
    file_paths["DefaultPath_out_0"] = os.path.join(file_dir, "out.0")
    file_paths["DefaultPath_out_1"] = os.path.join(file_dir, "out.1")
    file_paths["DefaultPath_arc_folder"] = os.path.join(file_dir, "arc\\")
    # file_paths["DefaultPath_out_dat"] = "/usr/local/src/sg/src/files/out.dat"
    # file_paths["DefaultPath_x_dat"] = "/usr/local/src/sg/src/files/x.dat"
    # file_paths["DefaultPath_out_0"] = "/usr/local/src/sg/src/files/out.0"
    # file_paths["DefaultPath_out_1"] = "/usr/local/src/sg/src/files/out.1"
    # file_paths["DefaultPath_arc_folder"] = "/usr/local/src/sg/src/files/arc"
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
