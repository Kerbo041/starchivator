from datetime import datetime
from model.TechnologicalParameter import TechnologicalParameter


class BufferArray:
    
    
    def __init__(self, max_buffer_length = 7277, time = None):
        self.buffer_array = []
        self.set_max_buffer_length(max_buffer_length)
        self.set_buffer_length(0)
        self.set_buffer_number(0)
        self.set_time(time)
    
    def get_length_of_buffer(self):
        return len(self.buffer_array)
    
    def set_max_buffer_length(self, max_buffer_length):
        self.max_buffer_length = max_buffer_length
    
    def flush_buffer(self):
        self.set_buffer_length(0)
        self.increase_buffer_number()
    
    def set_buffer_number(self, buffer_number):
        self.buffer_number = buffer_number
    
    def increase_buffer_number(self):
        self.buffer_number += 1
        
    def increase_buffer_length(self):
        self.buffer_length += 1
    
    def set_buffer_length(self, buffer_length = None):
        if buffer_length == None:
            self.buffer_length = len(self.buffer_array)
        else:
            self.buffer_length = buffer_length
            
    def add_element_to_array(self, technological_parameter:TechnologicalParameter):
        if self.buffer_length < self.max_buffer_length:
            if self.get_length_of_buffer() < self.max_buffer_length:
                self.buffer_array.append(technological_parameter)
            else:
                self.buffer_array[self.buffer_length] = technological_parameter
            self.increase_buffer_length()
            return True
        elif self.buffer_length == self.max_buffer_length:
            self.buffer_array.append(technological_parameter)
            self.flush_buffer()
            return False
        else:
            self.flush_buffer()
            return False
            
    def get_time(self):
        return self.time
            
    def set_time(self, time = None):
        if time:
            self.time = time
        else:
            self.time = datetime.now()
