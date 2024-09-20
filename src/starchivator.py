from src.config.config import get_config
from src.file_write.outdat_file_write import *
from src.file_write.xdat_file_write import *
from src.file_read.out_file_read import *
from src.file_read.parse_db import *
from src.data_check.check_data import *
import time

config_path = "src/config.json"

def main_cycle(values, file_paths):
    count = 0
    cycles = 0
    while True:
        new_data = file_read(file_paths['Path_out_0'])
        print("\nnew")
        for value in new_data:
            print(value["Value"], end="")
        changed = data_check(values, new_data)
        print("\nchanged")
        for value in changed:
            print(value["Value"], end="")
        values = new_data
        print("\n pre downwriting")
        changed_values_writing_check = write_changed_values(file_paths['Path_x_dat'], changed)
        print("afterwriting")
        if changed_values_writing_check:
            count += 1
        write_all_data_to_out_dat(file_paths['Path_out_dat'], values, count)
        print("dowrited")
        print("ccycled")
        time.sleep(0.5)
        cycles += 1
        if cycles > 100:
            break


def start():
    values = [{"number": i, "Value": b"\xff\xff\xff\xff"} for i in range(100)]
    config = get_config(config_path)
    file_paths = config["Paths"]
    write_all_data_to_out_dat(config['Path_out_dat'], values, 0)
    file_starter(config['Path_x_dat'])
    main_cycle(values, file_paths)
