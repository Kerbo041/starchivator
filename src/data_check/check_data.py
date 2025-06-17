from model.TechnologicalParameter import TechnologicalParameter
from model.TechnologicalParametersArray import TechnologicalParametersArray
from model.BufferArray import BufferArray
from model.Config import Config
from model.Logger import Logger


def compare_buffer_and_write_data_array(
    current_parameters_array: TechnologicalParametersArray,
    reading_parameters_array: TechnologicalParametersArray,
    buffer_parameters_array:BufferArray,
    config: Config,
    logger: Logger,
):
    buffered = True
    for iter in range(config.TOTAL_NUMBER_OF_VALUES):
        
        if current_parameters_array.parameters_array[iter] == reading_parameters_array.parameters_array[iter] or not reading_parameters_array.parameters_array[iter].state :
            pass
        else:
            current_parameters_array.parameters_array[iter].set_all_values_from_tuple(reading_parameters_array.parameters_array[iter].get_all_values())
            if buffered:
                buffered = buffer_parameters_array.add_element_to_array(reading_parameters_array.parameters_array[iter])
            else:
                pass
    current_parameters_array.set_time()