def check_data_array(values_old, values_new, count_of_values=200000):
    """## _summary_
        !!!delete count_of_values
        check length of arrays
    ### Args:
        - `values_old (_type_)`: _description_
        - `values_new (_type_)`: _description_
        - `count_of_values (int, optional)`: _description_. Defaults to 200000.

    ### Returns:
        - `_type_`: _description_
    """
    try:
        changed_values = []
        for i in range(count_of_values):
            if values_old[i] != values_new[i]:
                
                changed_values.append(
                    {
                        "Number": i,
                        "Value": values_new[i]["Value"],
                        "Signal": values_new[i]["Signal"],
                    }
                )
        print(changed_values)
        return changed_values
    except:
        return []
