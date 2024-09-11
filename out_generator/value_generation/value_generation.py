import datetime
import value_generation.generators as generators

def get_analog_value(type_a, start_of_interval, end_of_interval):
    types_of_generate = {
        "random": generators.generate_random_analog_value,
        "walking": generators.generate_walking_analog_value
    }
    return types_of_generate[type_a](start_of_interval, end_of_interval)
    
def get_discrete_value(type_d, length):
    types_of_generate = {
        "random": generators.generate_random_discrete_value
    }
    return types_of_generate[type_d](length)

def get_signal(type_s):
    types_of_generate = {
        "random": generators.generate_random_signal
    }
    return types_of_generate[type_s]()
    

def generate_analog_values(db_data, type_a, type_s):
    analog_values = []
    for db_value in db_data:
        now_time = datetime.datetime.now()
        value = get_analog_value(type_a, db_value["min"], db_value["max"])
        signal = get_signal(type_s)
        
        analog_values.append(
            {
                "number": db_value["number"],
                "time": now_time,
                "value": value,
                "signal": signal
            }
        )
    return analog_values

def generate_discrete_values(db_data, type_a, type_s):
    discrete_values = []
    for db_value in db_data:
        now_time = datetime.datetime.now()
        value = get_discrete_value(type_a, db_value["length"])
        signal = get_signal(type_s)
        
        discrete_values.append(
            {
                "number": db_value["number"],
                "time": now_time,
                "value": value,
                "signal": signal
            }
        )
    return discrete_values

def generate_update_values(start):
    now_time = datetime.datetime.now()
    hexabytes = ["11", "22", "33", "44", "55", "66", "77", "88", "99", "aa", "bb", "cc", "dd", "ee", "ff"]
    update_values = []
    iter = start
    for i in  hexabytes:
        update_values.append(
            {
                "number": iter,
                "time": now_time,
                "value": int("0x"+ (i*4), 16),
                "signal": generators.generate_random_update_signal()
            }
        )
        iter += 1
    return update_values