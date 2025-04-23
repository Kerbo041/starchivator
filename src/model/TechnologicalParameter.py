from model.TDateTime import TDateTime
from struct import pack, unpack
from model.Logger import Logger
from datetime import datetime


class TechnologicalParameter:
    # region Init

    def __init__(
        self,
        number=-1,
        time=None,
        value=b"\xff\xff\xff\xff",
        signal=b"\xff",
    ):
        self.set_number(number)
        self.set_time(time)
        self.set_value(value)
        self.set_signal(signal)
        self.state = self.check_state()

    # endregion

    # region Setters

    def set_number(self, number):
        if number is not None:
            if type(number) is int:
                self.number = number
            elif (type(number) is bytearray or type(number) is bytes) and len(
                number
            ) == 4:
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
        if (
            signal is not None
            and (type(signal) is bytearray or type(signal) is bytes)
            and len(signal) == 1
        ):
            self.signal = signal

    def set_time(self, time):
        if type(time) == datetime:
            self.time = time
        elif type(time) == float:
            self.time = TDateTime.tdatetime_to_datetime(self.time)
        elif (type(time) == bytearray or type(time)) == bytes and len(time) == 8:
            self.time = TDateTime.tdatetime_to_datetime(unpack("<d", time))

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
        return self.check_state()

    # endregion

    # region Checkers

    def __eq__(self, parameter):
        if type(parameter) == type(self) and (
            self.number == parameter.number
            and self.time == parameter.time
            and self.value == parameter.value
            and self.signal == parameter.signal
        ):
            return True
        else:
            return False

    def check_number(self):
        if self.number != -1 and self.number >= 0:
            return True

    def check_value(self):
        if self.value is not None and (
            type(self.value) == bytes or type(self.value) == bytearray
        ):
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

    def get_technological_parameter_from_bytes(self, bytes_array: bytearray):
        try:
            if len(bytes_array) < 17:
                return None
            number_in_bytes = bytes_array[0:4]
            if number_in_bytes == b"":
                return None
            number = unpack("<i", number_in_bytes)[0]
            if number == -1:
                return None
            time = bytes_array[4:12]
            value = bytes_array[12:16]
            signal = bytes_array[16:17]
            return TechnologicalParameter(number, time, value, signal)
        except Exception as exception:
            logger.log(exception)

    # endregion
