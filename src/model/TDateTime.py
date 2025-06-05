from datetime import datetime, timedelta


class TDateTime:

    # region Init

    def __init__(self, time_in_tdatetime = None, time_in_datetime: datetime = datetime.now()):
        if time_in_tdatetime and type(time_in_datetime) == float:
            self.set_time_in_TDateTime(time_in_tdatetime)
        elif time_in_datetime and type(time_in_datetime) == datetime:
            self.set_time_in_datetime
        else:
            self.set_time_in_datetime(datetime.now())

    # endregion

    # region Converting

    def tdatetime_to_datetime(tdatetime: float) -> datetime:
        return datetime(1899, 12, 30) + timedelta(days=tdatetime)

    def datetime_to_tdatetime(time_in_datetime: datetime = datetime.now()):
        delta_time = time_in_datetime - datetime(1899, 12, 30)
        tdatetime = delta_time.total_seconds() / 3600 / 24
        return tdatetime

    # endregion

    # region Setters

    def set_time_in_datetime(self, time_in_datetime: datetime = datetime.now()):
        self.time_in_datetime = time_in_datetime
        self.time_in_TDateTime = self.datetime_to_tdatetime(self.time_in_datetime)

    def set_time_in_TDateTime(self, time_in_TDateTime: float):
        self.time_in_TDateTime = time_in_TDateTime
        self.time_in_datetime = self.tdatetime_to_datetime(time_in_TDateTime)

    # endregion

    # region Getters

    def get_time_in_datetime(self) -> datetime:
        return self.time_in_datetime

    def get_time_in_TDateTime(self) -> float:
        return self.time_in_TDateTime

    # endregion

    def __str__(self) -> str:
        return str(self.time_in_datetime)
