
def check_data_array(values_old, values_new):
    if len(values_old) != len(values_new):
        print("check data: length error")
    array_of_changed_signals = {}
    for i in range(200000):
        for key in values_old[i]:
            if values_old[i][key] != values_new[i][key]:
                array_of_changed_signals[i] = values_new[i]
    return array_of_changed_signals
