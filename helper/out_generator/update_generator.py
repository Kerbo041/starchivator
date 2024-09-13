import file_read_and_write.dataparse as dataparse
import value_generation.value_generation as value_generation
import file_read_and_write.bytecoder as bytecoder
import file_read_and_write.outwriter as outwriter
import config.config as config
import datetime
import time
import out_gen_checker
import file_read_and_write.updater as updater
import random
import sys

def look_out_x(console_arg):
    i = int(console_arg)
    cursor_points_0 = [20, 60, 100, 500]
    # point_0 =  cursor_points_0[random.randint(0, len(cursor_points_0) - 1)]
    point_0 =  cursor_points_0[i]
    
    cursor_points_1 = [20, 60, 100, 500]
    # point_1 = cursor_points_1[random.randint(0, len(cursor_points_1) - 1)]
    point_1 = cursor_points_1[i]
    
    update_values = value_generation.generate_update_values(point_0)
    byte_update = bytecoder.bytecoder(update_values)
    updater.write_new_values(config.out_0_path, byte_update, point_0)
        
    update_values = value_generation.generate_update_values(point_1)
    byte_update = bytecoder.bytecoder(update_values)
    updater.write_new_values(config.out_1_path, byte_update, point_1)
        

look_out_x(sys.argv[1])