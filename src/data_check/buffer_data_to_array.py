from model.logger import logger

def buffer_data(
    buffer_array,
    changed_values,
    current_parameter_index,
    special_buffer_signal,
    # buffer_size=7279,
    buffer_size=7277,
):
    for value in changed_values:
        if current_parameter_index == buffer_size:
            buffer_array[current_parameter_index] = value
            # print(f"buffered, current index is {current_parameter_index}, buffer signal was {special_buffer_signal}. reason is index == buffer_size")
            # print(f"array of changed values has length {len(changed_values)}")
            # for value in changed_values:
            #     print(value, end=" ")
            # print("")
            
            current_parameter_index = 0
            special_buffer_signal += 1
            break
        elif current_parameter_index > buffer_size:
            current_parameter_index = 0
            special_buffer_signal += 1
            break
        else:
            buffer_array[current_parameter_index] = value
            current_parameter_index += 1
    # logger.debug_log(f"array of changed values has length {len(changed_values)}")
    return buffer_array, current_parameter_index, special_buffer_signal
