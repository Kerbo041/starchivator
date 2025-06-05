from datetime import datetime
from model.TechnologicalParameter import TechnologicalParameter


class BufferArray:
    
    
    def __init__(self):
        self.buffer_array = []
        self.time = datetime.now()
        self.set_buffer_size()
        self.set_buffer_number(0)
    
    def flush_buffer(self):
        self.buffer_array = []
        self.set_buffer_size()
        self.increase_buffer_number()
    
    def set_buffer_number(self, buffer_number):
        self.buffer_number = buffer_number
    
    def increase_buffer_number(self):
        self.buffer_number += 1
    
    def set_buffer_size(self):
        self.buffer_size = len(self.buffer_array)
        
    def add_element_to_array(self, technological_parameter:TechnologicalParameter):
        if technological_parameter.state == True:
            self.buffer_array.append(technological_parameter)