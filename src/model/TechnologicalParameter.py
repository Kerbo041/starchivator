from model.TDateTime import TDateTime


class TechnologicalParameter:

    def __init__(
        self,
        Number=-1,
        NumberInBytes=b"\xff\xff\xff\xff",
        Time=b"\xff\xff\xff\xff\xff\xff\xff\xff",
        Value=b"\xff\xff\xff\xff",
        Signal=b"\xff",
        State=False,
    ):

        self.Number = Number
        self.NumberInBytes = NumberInBytes
        self.Time = Time
        self.Value = Value
        self.Signal = Signal
        self.State = State

    def get_date(self):
        return TDateTime.tdatetime_to_datetime(self.Time)
