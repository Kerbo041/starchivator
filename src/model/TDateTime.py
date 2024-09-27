from datetime import datetime, timedelta

class TDateTime:
    def __init__(self, time_in_datetime: datetime = datetime.now()) -> None:
        self.set_time(time_in_datetime)
    
    def tdatetime_to_datetime(tdatetime: float) -> datetime:
        return datetime(1899, 12, 30) + timedelta(days=tdatetime)
    
    def datetime_to_tdatetime(time_in_datetime: datetime = datetime.now()) -> bytes:
        delta_time =  time_in_datetime - datetime(1899, 12, 30)
        tdatetime = delta_time.total_seconds()/3600/24
        return  tdatetime 
    
    
    def __str__(self) -> str:
        return str(self.time)
    
    def set_time(self, time_in_datetime: datetime = datetime.now()) -> None:
        self.time = time_in_datetime
            
    def set_tdatetime(self, time_in_tdatetime: float = tdatetime_to_datetime(datetime.now())) -> None:
            self.time = self.tdatetime_to_datetime(time_in_tdatetime)
            
    def get_time(self) -> datetime:
        return self.time
    
    def get_tdatetime(self) -> float:
        return self.datetime_to_tdatetime(self.time)
    