import file_read_and_write.dataparse as dataparse
import value_generation.value_generation as value_generation
import file_read_and_write.bytecoder as bytecoder
import file_read_and_write.outwriter as outwriter
import config.config as config
import datetime
import time
import out_gen_checker
import file_read_and_write.updater as updater

def make_out():
    db_a_data = dataparse.reader_db_a(config.db_a_path)
    db_d_data = dataparse.reader_db_d(config.db_d_path)
    
    
    while True:
        values_a = value_generation.generate_analog_values(db_a_data, "walking", "random")
        values_d = value_generation.generate_discrete_values(db_d_data, "random", "random")
        bytes_a_values = bytecoder.bytecoder(values_a)
        bytes_d_values = bytecoder.bytecoder(values_d)
        outwriter.outwriter(bytes_a_values, config.out_0_path)
        outwriter.outwriter(bytes_d_values, config.out_1_path)
        print(datetime.datetime.now())
        
def make_one():
    db_a_data = dataparse.reader_db_a(config.db_a_path)
    db_d_data = dataparse.reader_db_d(config.db_d_path)
    values_a = value_generation.generate_analog_values(db_a_data, "walking", "random")
    values_d = value_generation.generate_discrete_values(db_d_data, "random", "random")
    bytes_a_values = bytecoder.bytecoder(values_a)
    bytes_d_values = bytecoder.bytecoder(values_d)
    outwriter.outwriter(bytes_a_values, config.out_0_path)
    outwriter.outwriter(bytes_d_values, config.out_1_path)

def look_out():
    print("start cheeking")
    db_a_data = dataparse.reader_db_a(config.db_a_path)
    db_d_data = dataparse.reader_db_d(config.db_d_path)
    
    
    
    values_a = value_generation.generate_analog_values(db_a_data, "walking", "random")
    values_d = value_generation.generate_discrete_values(db_d_data, "random", "random")
    bytes_a_values = bytecoder.bytecoder(values_a)
    bytes_d_values = bytecoder.bytecoder(values_d)
    outwriter.outwriter(bytes_a_values, config.out_0_path)
    outwriter.outwriter(bytes_d_values, config.out_1_path)
    print(datetime.datetime.now())
    read_path = "C:\\spd3\\dat\\out.dat"
    time.sleep(7)
    out_dat_values = out_gen_checker.get_data_from_dat_file(read_path)
    out_gen_checker.apply_analog_and_discrets(bytes_a_values, bytes_d_values, out_dat_values)
    

def look_out_x():
    print("start cheeking")
    db_a_data = dataparse.reader_db_a(config.db_a_path)
    db_d_data = dataparse.reader_db_d(config.db_d_path)
    
    
    
    values_a = value_generation.generate_analog_values(db_a_data, "walking", "random")
    values_d = value_generation.generate_discrete_values(db_d_data, "random", "random")
    bytes_a_values = bytecoder.bytecoder(values_a)
    bytes_d_values = bytecoder.bytecoder(values_d)
    outwriter.outwriter(bytes_a_values, config.out_0_path)
    outwriter.outwriter(bytes_d_values, config.out_1_path)
    print(datetime.datetime.now())
    
    time.sleep(10)
    
    updated_a_values = values_a
    updated_d_values = values_d
    
    cursor_points_0 = [20, 1000]
    cursor_points_1 = [100000, 100050 ]
    for point in cursor_points_0:
        update_values = value_generation.generate_update_values(point)
        byte_update = bytecoder.bytecoder(update_values)
        updater.write_new_values(config.out_0_path, byte_update, point)
        iter = point
        for value in update_values:
            updated_a_values[iter]["value"] = value["value"]
            iter += 1
            
    for point in cursor_points_1:
        update_values = value_generation.generate_update_values(point)
        byte_update = bytecoder.bytecoder(update_values)
        updater.write_new_values(config.out_1_path, byte_update, point)
        iter = point
        for value in update_values:
            updated_d_values[iter]["value"] = value["value"]
            iter += 1
    
    
    out_dat_values = dataparse.get_data_from_out_dat_file(config.out_dat_path)
    x_dat_values = dataparse.get_data_from_x_dat_file(config.x_dat_path)
    updated_bytes_a_values = bytecoder.bytecoder(updated_a_values)
    updated_bytes_d_values = bytecoder.bytecoder(updated_d_values)
    out_gen_checker.check_x_file(updated_bytes_a_values, updated_bytes_d_values, out_dat_values, x_dat_values)
    

make_one()