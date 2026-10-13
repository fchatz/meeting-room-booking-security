from datetime import datetime
from datetime import timedelta


def calculate_end_time(start_time: str):
    one_hour = timedelta(hours=1)
    start = datetime.strptime(start_time, "%H:%M")
    start += one_hour
    formatted = start.strftime("%H:%M")
    return formatted
