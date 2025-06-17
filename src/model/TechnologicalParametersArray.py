from datetime import datetime
from model.TechnologicalParameter import TechnologicalParameter


class TechnologicalParametersArray:

    def __init__(self,parameters_array = None, total_number_of_parameters = 200000, time = None):
        self.total_number_of_parameters = total_number_of_parameters
        if parameters_array == None:
            self.set_empty_parameters_array()
        else: 
            self.parameters_array = parameters_array
        self.number_of_valid_parameters = self.set_number_of_valid_parameters()
        self.set_time()
        
    def set_time(self, time = None):
        if time:
            self.time = time
        else:
            self.time = datetime.now()

    def set_empty_parameters_array(self):
        self.parameters_array = []
        for i in range(self.total_number_of_parameters):
            self.parameters_array.append(TechnologicalParameter())
    
    def set_number_of_valid_parameters(self):
        number_of_valid_parameters = 0
        for parameter in self.parameters_array:
            if type(parameter) == TechnologicalParameter:
                if parameter.get_state():
                    number_of_valid_parameters += 1
        self.number_of_valid_parameters = number_of_valid_parameters
    
    def check_length_of_number_of_parameters(self):
        return len(self.ParametersArray) == self.total_number_of_parameters

    def append_empty_values_to_array(self):
        self.set_number_of_valid_parameters()
        if not self.check_length_of_number_of_parameters():
            for i in range(self.number_of_valid_parameters, self.total_number_of_parameters):
                self.parameters_array.append(TechnologicalParameter())
    
    def get_time(self):
        return self.time
        