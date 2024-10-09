

def buffer_data(buffer_array, changed_values, current_parameter_index, buffer_size = 7279):
    for value in changed_values:
        if current_parameter_index >= buffer_size:
            current_parameter_index = 0
            break
        buffer_array[current_parameter_index] = value
        current_parameter_index += 1
    return buffer_array, current_parameter_index