def check_data_array(values_old, values_new, count_of_values=200000):
    try:
        array_of_changed_signals = []
        for i in range(count_of_values):
            if values_old[i] != values_new[i]:
                array_of_changed_signals.append(
                    {
                        "Number": i,
                        "Value": values_new[i]["Value"],
                        "Signal": values_new[i]["Signal"],
                    }
                )
        return array_of_changed_signals
    except:
        return []
