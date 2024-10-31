# from src.file_write.outdat_file_write import out_dat_file_write
# from src.file_write.xdat_file_write import write_changed_values
# from src.data_check.check_data import check_data_array
# from src.file_read.out_file_read import read_out_file
# from src.config.config import get_config
from file_write.outdat_file_write import out_dat_file_write
from file_write.xdat_file_write import x_dat_file_write
from file_write.archive_file_write import archive_file_write
from data_check.check_data import check_data_array
from data_check.buffer_data_to_array import buffer_data
from file_read.out_file_read import get_out_data
from file_read.out_file_read_buffered import get_out_data_with_buffer
from config.config import get_config
from datetime import datetime
import time


def main_cycle(values, file_paths, headers):
    current_values = values
    special_buffer_signal = 0
    current_parameter_index = 0
    BLOCK_NUMBER = 3
    array_of_buffered_parameters = {}
    current_time = datetime(1, 1,1)
    print("Packing started")
    while True:
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
        file_name_archive = f"{current_time.year}{current_time.month}{current_time.day}.VO{BLOCK_NUMBER}"
        
        readed_new_data = get_out_data_with_buffer(
            file_paths["Path_out_0"],
            file_paths["Path_out_1"],
            analog_count=20000,
            discrete_count=180000,
        )
        if readed_new_data == 0:
            print("EMPTY FILE")
            continue
        # readed_new_data = get_out_data(
        #     file_paths["Path_out_0"],
        #     file_paths["Path_out_1"],
        #     analog_count=20000,
        #     discrete_count=180000,
        # )

        changed_values = check_data_array(current_values, readed_new_data)

        array_of_buffered_parameters, current_parameter_index, special_buffer_signal = buffer_data(
            array_of_buffered_parameters, changed_values, current_parameter_index, special_buffer_signal
        )

        current_values = readed_new_data

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
            file_name_archive,
            headers["Archive"],
            current_values, 
            changed_values,
            current_time,
            is_new_hour,
            is_new_day
            )
        time_packing = (datetime.now() - current_time).total_seconds()
        # print(f"Packing cycle done, writing time is {time_packing}")
        # print(f"special_buffer_signal is {special_buffer_signal}")
        # print(f"current_parameter_index is {current_parameter_index}")
        if time_packing < 0.5:
            time.sleep(0.5 - time_packing)


def start(config_path="src/config.json", header_text="StarPack____"):
    config = get_config(config_path)
    file_paths = config["Paths"]
    headers = config["HeaderTexts"]
    values = {
        i: {
            "Value": b"\xff\xff\xff\xff",
            "Signal": b"\xff",
        }
        for i in range(200000)
    }
    main_cycle(values, file_paths, headers)


start(
    config_path="c:\\Users\\NOVOSELOV_G\\Documents\\GitHub\\starchivator\\src\\config.json"
)
