

def data_change(values_old, values_new):
    for i in values_new:
        if values_new[i]["Status"]:
            values_old[i] = values_new[i]