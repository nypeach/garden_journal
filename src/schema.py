"""
Garden Journal Data Schema
Defines the structure for garden_data.json and provides validation functions.
"""

import re
from dataclasses import dataclass, field
from typing import List, Optional, Dict


def validate_plant_id(plant_id: str) -> bool:
    """Validate plant_id format: {planttype}_{number}"""
    pattern = r'^[a-z_]+_\d{3}$'
    return bool(re.match(pattern, plant_id))


def validate_date(date_str: str) -> bool:
    """Validate date format: YYYYMMDD"""
    if not re.match(r'^\d{8}$', date_str):
        return False

    try:
        year = int(date_str[:4])
        month = int(date_str[4:6])
        day = int(date_str[6:8])

        if not (1900 <= year <= 2100):
            return False
        if not (1 <= month <= 12):
            return False
        if not (1 <= day <= 31):
            return False

        return True
    except ValueError:
        return False


def validate_time(time_str: str) -> bool:
    """Validate time format: HHMM (military/24-hour time)"""
    if not re.match(r'^\d{4}$', time_str):
        return False

    try:
        hour = int(time_str[:2])
        minute = int(time_str[2:])
        return 0 <= hour <= 23 and 0 <= minute <= 59
    except ValueError:
        return False


def validate_photo_filename(filename: str) -> bool:
    """Validate photo filename format: {plant_id}_{YYYYMMDD}_{HHMM}_{seq}.jpg"""
    pattern = r'^[a-z_]+_\d{3}_\d{8}_\d{4}_\d+\.jpg$'

    if not re.match(pattern, filename):
        return False

    parts = filename.replace('.jpg', '').split('_')
    if len(parts) < 5:
        return False

    plant_id = f"{parts[0]}_{parts[1]}"
    date = parts[2]
    time = parts[3]

    return (validate_plant_id(plant_id) and
            validate_date(date) and
            validate_time(time))


def format_date_display(date_str: str) -> str:
    """Format a date string (YYYYMMDD) for display"""
    if not validate_date(date_str):
        return date_str

    months = [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ]

    year = int(date_str[:4])
    month = int(date_str[4:6])
    day = int(date_str[6:8])

    return f"{months[month-1]} {day}, {year}"


def format_time_display(time_str: str) -> str:
    """Format a time string (HHMM) for display in 12-hour format"""
    if not validate_time(time_str):
        return time_str

    hour = int(time_str[:2])
    minute = int(time_str[2:])

    period = "AM" if hour < 12 else "PM"
    display_hour = hour if hour <= 12 else hour - 12
    if display_hour == 0:
        display_hour = 12

    return f"{display_hour}:{minute:02d} {period}"


if __name__ == "__main__":
    # Test validation functions
    print("Testing validation functions...")

    assert validate_plant_id("basil_001") == True
    assert validate_plant_id("basil001") == False
    print("✓ Plant ID validation working")

    assert validate_date("20251105") == True
    assert validate_date("2025-11-05") == False
    print("✓ Date validation working")

    assert validate_time("0745") == True
    assert validate_time("2400") == False
    print("✓ Time validation working")

    assert validate_photo_filename("basil_001_20251105_0745_1.jpg") == True
    assert validate_photo_filename("basil_20251105_0745_1.jpg") == False
    print("✓ Photo filename validation working")

    print("\n✅ All validation tests passed!")
