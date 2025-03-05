def check_data_array(values_old, values_new):
    if len(values_old) != len(values_new):
        return ["ERROR"]
    changed_values = []
    for i in range(len(values_new)):
        if values_new[i]["Status"] or True:
            if (values_old[i]["Value"] != values_new[i]["Value"] or values_old[i]["Signal"] != values_new[i]["Signal"]):
                changed_values.append(
                    {
                        "Number": i,
                        "Value": values_new[i]["Value"],
                        "Signal": values_new[i]["Signal"],
                        "Status": values_new[i]["Status"],
                        
                    }
                )
    return changed_values
