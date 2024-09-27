from struct import pack, unpack
from src.model.TDateTime import TDateTime


class OutFile:

    def __init__(self, file_path, line_length=17):
        self.file_path = file_path
        self.line_length = line_length
        self.file = open(file_path, "rb")
        self.cursor_position = self.get_cursor_position()

    def read_current_line_in_bytes(self):
        return {
            "NumberInBytes": self.file.read(4),
            "TDateTimeInBytes": self.file.read(8),
            "ValueInBytes": self.file.read(4),
            "SignalInBytes": self.file.read(1),
        }

    def set_cursor_position(self, number_of_line):
        self.file.seek(number_of_line * self.line_length)

    def get_cursor_position(self):
        self.cursor_position = self.file.tell()
        return self.cursor_position

    def read_line(self, number_of_line):
        self.set_cursor_position(number_of_line)
        return self.conver_line_from_bytes(self.read_current_line_in_bytes(self))

    def conver_line_from_bytes(self, line_in_bytes):
        return {
            "Number": unpack("<i", line_in_bytes["NumberInBytes"]),
            "Datetime": TDateTime.tdatetime_to_datetime(
                unpack("<d", line_in_bytes["TDateTimeInBytes"])
            ),
            "ValueInBytes": line_in_bytes["ValueInBytes"],
            "SignalInBytes": line_in_bytes["SignalInBytes"],
        }
