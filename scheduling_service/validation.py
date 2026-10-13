from contextlib import closing
from datetime import date,datetime,time
from scheduling_helper.time_utils import calculate_end_time

def is_weekday(date_string: str) -> bool:
     booking_date = date.fromisoformat(date_string)
     booking_date = booking_date.weekday()
     return booking_date < 5

def is_within_working_hours(start_time: str) -> bool:
    opening_time = time(9,0 )
    closing_time = time(17,0 )
    start = datetime.strptime(start_time, "%H:%M").time()
    stop = calculate_end_time(start_time)
    stop = datetime.strptime(stop, "%H:%M").time()
    return start >= opening_time and stop <= closing_time and stop > start

def validate_schedule(date_string: str, start_time: str) -> bool:
    return is_weekday(date_string) and is_within_working_hours(start_time)
