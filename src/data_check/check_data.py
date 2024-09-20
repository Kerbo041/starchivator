
def check_data(values_old, values_new):
    if len(values_old) != len(values_new):
        print("check data: length error")
    data_keys = ["Number", "Date", "Value", "Signal"]
    array_of_changed_signals = []
    for i in range(200000):
        check =  False
        for key in data_keys:
            if values_old[i][key] != values_new[i][key]:
                check = True
        if check:
            array_of_changed_signals.append(values_new[i])
    return array_of_changed_signals

def data_check(old, new):
    changed = []
    for value in new:
        if value["Value"] != old[value["Number"]]["Value"]:
            changed.append(value)
    return changed