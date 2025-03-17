from datetime import datetime
from model.TechnologicalParameter import TechnologicalParameter


class TechnologicalParametersArray:

    def __init__(self, total_number_of_parameters = 200000):
        self.Time = datetime.now()
        self.total_number_of_parameters = total_number_of_parameters
        self.ParametersArray = self.get_empty_parameters_array()
        self.CurrentSyncronisationValue = 0
        self.CurrentBufferValue = 0
        self.Buffer = []
        

    def get_empty_parameters_array(self):
        parameters_array = []
        for i in range(self.total_number_of_parameters):
            parameters_array.append(TechnologicalParameter())
            
    def check_number_of_parameters(self):
        return len(self.ParametersArray) == self.total_number_of_parameters

