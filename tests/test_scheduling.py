from scheduling_service.validation import is_weekday, is_within_working_hours, validate_schedule
from scheduling_helper.time_utils import calculate_end_time


def test_weekday():
    assert is_weekday("2026-10-14") == True

def test_weekend():
    assert is_weekday("2026-10-17") == False

def test_working_hours():
    assert is_within_working_hours("16:30") == False

def test_working_hours_boundaries():
    assert is_within_working_hours("09:00") == True
    assert is_within_working_hours("16:00") == True
    assert is_within_working_hours("08:30") == False
    assert is_within_working_hours("23:30") == False

def test_complete_schedule():
    assert validate_schedule("2026-10-13", "10:00") == True
    assert validate_schedule("2026-10-17", "10:00") == False
    assert validate_schedule("2026-10-13", "23:00") == False

def test_helper_end_time():
    assert calculate_end_time("10:00") == "11:00"
    assert calculate_end_time("16:00") == "17:00"
