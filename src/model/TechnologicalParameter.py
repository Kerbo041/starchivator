from model.TDateTime import TDateTime
from struct import pack, unpack
from model.logger import logger
class TechnologicalParameter:


    # region Init
    
    def __init__(
        self,
        number=-1,
        time_in_TDateTime=b"\xff\xff\xff\xff\xff\xff\xff\xff",
        time = None,
        value=b"\xff\xff\xff\xff",
        signal=b"\xff",
        state=False,
        logger = None
    ):
        self.set_number(number)
        self.time = time
        self.value = value
        self.signal = signal
        self.state = state
        
    # endregion
    
    # region Setters
    
    def set_number(self, number):
        if number is not None:
            if type(number) is int:
                self.number = number
            elif (type(number) is bytearray or type(number) is bytes) and len(number) == 4:
                self.number = unpack("<i", number)
        else:
            self.number = -1
    
    def set_value(self, value):
        if value is not None:
            if (type(value) is bytearray or type(value) is bytes) and len(value) == 8:
                self.value = value
            else:
                self.value = b"\xff\xff\xff\xff\xff\xff\xff\xff"
        else:
            self.value = b"\xff\xff\xff\xff\xff\xff\xff\xff" 

    def set_signal(self, signal):
        self.signal = signal
    
    def set_time_in_datetime(self, time):
        self.time = time
        self.time_in_TDateTime = TDateTime.datetime_to_tdatetime(self.time)
        self.time_in_TDateTime_in_bytes = pack("<d", self.time_in_TDateTime)

    # endregion
    
    # region Getters
    
    def get_time(self):
        return self.time
    
    def get_time_in_tdatetime(self):
        return TDateTime.datetime_to_tdatetime(self.time)
    
    def get_value(self):
        return self.value
    
    def get_number(self):
        return self.number
    
    def get_number_in_bytes(self):
        return pack("<i", self.number)
    
    def get_state(self):
        return self.state
    
    # endregion
    
    # region Checkers
    
    def check_number(self):
        if self.number != -1 and self.number >= 0:
            return True
        
    def check_value(self):
        if self.value is not None and (type(self.value) == bytes or type(self.value) == bytearray):
            return True
        else:
            return False
    
    def check_state(self):
        if self.check_number() and self.check_value():
            self.state = True
        else:
            self.state = False
    
    # endregion
    
    # region Creation
    
    
    
    def get_technological_parameter_from_bytes(self, bytes_array:bytearray):
        try:
            if len(bytes_array) < 17:
                return None
            number_in_bytes = bytes_array[0:4]
            if number_in_bytes == b"":
                return None
            number = unpack("<i", number_in_bytes)[0]
            if number == -1:
                return None
            date = bytes_array[4:12]
            value = bytes_array[12:16]
            signal = bytes_array[16:17]
            status = True
            return TechnologicalParameter(number, number_in_bytes, date, value, signal, status)
        except Exception as exception:
            logger.log(exception)
            
    # endregion