"""
=================================================================
Garden Journal Data Schema
VERSION: 13.1
Last Updated: 2025-11-12
=================================================================

Defines the structure for garden_data.json and provides validation functions.

Major Changes in Version 13.1:
- Added 'summary' field to Plant dataclass for evolving plant assessments
- Support for multiple observations per plant per day (with timestamps)
- Photo metadata (before/after tags, observation linking)
- Detailed action tracking (amounts, products, methods)
- Soil moisture field with descriptions
- Temporary location tracking (indoors/covered/protected)
- Position field for plants sharing containers
- Upcoming actions array
- Product/brand tracking in actions
- Container_name added for grouping plants
- Stake number support for staked containers
"""

import re
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any


# ============================================================================
# Location and Container Structures
# ============================================================================

@dataclass
class LocationHistoryEntry:
    """A single location history record for a plant"""
    date: str  # YYYYMMDD
    location: str  # Physical location (Picnic Table, Panel 1, Indoors, etc.)
    container_name: str  # Friendly name (Basil Pot - Left, Pepper Box, etc.)
    container_type: str  # Technical description
    stake: Optional[int] = None  # Stake number if applicable (1, 2, 3, 4)
    position: Optional[str] = None  # For shared containers: "edges", "center", "left side"
    soil_mix: str = ""
    reason: str = ""
    transplant_method: Optional[str] = None


@dataclass
class TemporaryLocation:
    """Temporary location change (brought indoors, covered, etc.)"""
    date: str  # YYYYMMDD
    time: str  # HHMM
    temp_location: str  # "Indoors", "Covered", "Garage", etc.
    reason: str  # "Cold protection", "Frost warning", etc.
    returned_date: Optional[str] = None  # When returned to normal location
    returned_time: Optional[str] = None


# ============================================================================
# Plant Care and Tracking
# ============================================================================

@dataclass
class CareAction:
    """A detailed care action record"""
    date: str  # YYYYMMDD
    time: str  # HHMM
    action_type: str  # watering, pruning, treatment, feeding, mulching, etc.
    details: str  # Description of what was done
    amount: Optional[str] = None  # "1½ cups", "16 oz", "½ cup", etc.
    product: Optional[str] = None  # "Captain Jack's Neem Oil", "Miracle-Gro Organic Choice"
    method: Optional[str] = None  # "hose gentle shower", "misting", "at base", etc.
    notes: Optional[str] = None


@dataclass
class GrowthStageEntry:
    """A single growth stage milestone"""
    date: str  # YYYYMMDD
    stage: str
    notes: str


@dataclass
class Plant:
    """A single plant entity"""
    plant_id: str
    common_name: str
    purchase_date: str  # YYYYMMDD
    status: str  # active, removed, died, harvested
    location_history: List[LocationHistoryEntry]
    current_location: Dict[str, Any]
    variety: Optional[str] = None
    source: Optional[str] = None
    summary: Optional[str] = None
    care_history: List[CareAction] = field(default_factory=list)
    growth_stages: List[GrowthStageEntry] = field(default_factory=list)
    temporary_locations: List[TemporaryLocation] = field(default_factory=list)


# ============================================================================
# Daily Observation Structures
# ============================================================================

@dataclass
class Weather:
    """Weather information for a day or observation"""
    temp_high: Optional[int] = None
    temp_low: Optional[int] = None
    conditions: Optional[str] = None
    sunrise: Optional[str] = None  # HHMM
    sunset: Optional[str] = None   # HHMM
    humidity: Optional[int] = None
    wind: Optional[str] = None
    notes: Optional[str] = None


@dataclass
class PhotoMetadata:
    """Metadata for a photo"""
    filename: str  # e.g., basil_001_20251111_1400_1.jpg
    timestamp: str  # HHMM when photo was taken
    tags: List[str] = field(default_factory=list)  # ["before_pruning", "after_watering", etc.]
    caption: Optional[str] = None


@dataclass
class PlantObservation:
    """Single observation of a plant at a specific time"""
    plant_id: str
    time: str  # HHMM - when this observation was made
    location: str
    container_name: str
    container_type: str
    stake: Optional[int] = None
    position: Optional[str] = None
    soil_mix: str = ""
    soil_moisture: Optional[str] = None  # "bone dry", "lightly moist", "very dry", etc.
    current_stage: str = ""
    next_stage: str = ""
    observations: str  = "" # What you observed
    actions_taken: List[str] = field(default_factory=list)  # Actions during this observation
    notes: str = ""
    plant_qa: Optional[Dict[str, str]] = None  # {"question": "...", "answer": "..."}
    photos: List[PhotoMetadata] = field(default_factory=list)


@dataclass
class QuestionAnswer:
    """A Q&A pair from garden discussions"""
    question: str
    answer: str


@dataclass
class UpcomingAction:
    """Planned future action"""
    description: str
    target_date: Optional[str] = None  # YYYYMMDD if specific date known
    target_timeframe: Optional[str] = None  # "in a few days", "next week", etc.
    plants_affected: List[str] = field(default_factory=list)  # List of plant_ids


@dataclass
class DailyEntry:
    """A complete daily journal entry"""
    date: str  # YYYYMMDD
    time_of_entry: str  # HHMM - when you started the entry
    weather: Optional[Weather] = None
    activities: List[str] = field(default_factory=list)
    observations: List[str] = field(default_factory=list)
    questions_and_answers: List[QuestionAnswer] = field(default_factory=list)
    upcoming_actions: List[UpcomingAction] = field(default_factory=list)
    plant_observations: List[PlantObservation] = field(default_factory=list)


@dataclass
class GardenData:
    """Root data structure"""
    metadata: Dict[str, str]
    plants: List[Plant]
    locations: Dict[str, Dict]
    daily_entries: List[DailyEntry]


# ============================================================================
# Validation Functions
# ============================================================================

def validate_plant_id(plant_id: str) -> bool:
    """
    Validate plant_id format: {planttype}_{number}

    Valid: basil_001, tomato_001, strawberry_002
    Invalid: basil001, basil_1, Basil_001
    """
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


def validate_plant_status(status: str) -> bool:
    """Validate plant status value"""
    valid_statuses = {'active', 'removed', 'died', 'harvested'}
    return status in valid_statuses


def validate_action_type(action_type: str) -> bool:
    """Validate action type"""
    valid_actions = {
        'watering', 'pruning', 'treatment', 'feeding', 'mulching',
        'transplanting', 'seeding', 'thinning', 'staking', 'covering',
        'observation', 'moving', 'soil_amendment', 'pest_control'
    }
    return action_type in valid_actions


# ============================================================================
# Helper Functions
# ============================================================================

def parse_photo_filename(filename: str) -> Optional[Dict[str, str]]:
    """Parse a photo filename into its components"""
    if not validate_photo_filename(filename):
        return None

    parts = filename.replace('.jpg', '').split('_')

    return {
        'plant_id': f"{parts[0]}_{parts[1]}",
        'date': parts[2],
        'time': parts[3],
        'sequence': parts[4]
    }


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


def generate_plant_id(plant_type: str, existing_ids: List[str]) -> str:
    """Generate the next available plant ID for a given plant type"""
    plant_type = plant_type.lower().replace(' ', '_')

    existing_numbers = []
    for plant_id in existing_ids:
        if plant_id.startswith(f"{plant_type}_"):
            try:
                num = int(plant_id.split('_')[-1])
                existing_numbers.append(num)
            except ValueError:
                continue

    next_num = 1 if not existing_numbers else max(existing_numbers) + 1

    return f"{plant_type}_{next_num:03d}"


def group_plants_by_container(plant_observations: List[PlantObservation]) -> Dict[str, List[PlantObservation]]:
    """
    Group plant observations by their container for display purposes.

    Returns a dict with keys like:
    - "Panel 1 - Basil Pot - Left" (single plant)
    - "Panel 7 - Pepper Box" (multiple plants with stakes)
    - "Raised Bed - Panels 16-18" (multiple plants with stakes)
    """
    grouped = {}

    for obs in plant_observations:
        # Create grouping key
        if obs.stake:
            # This plant has a stake, group by location + container_name
            key = f"{obs.location} - {obs.container_name}"
        else:
            # No stake, group by location + container_name + plant
            key = f"{obs.location} - {obs.container_name}"

        if key not in grouped:
            grouped[key] = []
        grouped[key].append(obs)

    return grouped


# ============================================================================
# Example Usage and Tests
# ============================================================================

if __name__ == "__main__":
    print("=" * 65)
    print("Garden Journal Schema Validation Tests")
    print("VERSION: 13")
    print("=" * 65)
    print()

    # Test validation functions
    print("Testing validation functions...")

    # Plant IDs
    assert validate_plant_id("basil_001") == True
    assert validate_plant_id("basil001") == False
    assert validate_plant_id("Basil_001") == False
    print("✓ Plant ID validation working")

    # Dates
    assert validate_date("20251105") == True
    assert validate_date("2025-11-05") == False
    assert validate_date("20251305") == False
    print("✓ Date validation working")

    # Times
    assert validate_time("0745") == True
    assert validate_time("1430") == True
    assert validate_time("2400") == False
    print("✓ Time validation working")

    # Photo filenames
    assert validate_photo_filename("basil_001_20251105_0745_1.jpg") == True
    assert validate_photo_filename("basil_20251105_0745_1.jpg") == False
    print("✓ Photo filename validation working")

    # Action types
    assert validate_action_type("watering") == True
    assert validate_action_type("pruning") == True
    assert validate_action_type("invalid") == False
    print("✓ Action type validation working")

    # Parse photo filename
    parsed = parse_photo_filename("basil_001_20251105_0745_1.jpg")
    assert parsed['plant_id'] == "basil_001"
    assert parsed['date'] == "20251105"
    assert parsed['time'] == "0745"
    print("✓ Photo filename parsing working")

    # Format date
    assert format_date_display("20251105") == "November 5, 2025"
    print("✓ Date formatting working")

    # Format time
    assert format_time_display("0745") == "7:45 AM"
    assert format_time_display("1430") == "2:30 PM"
    print("✓ Time formatting working")

    # Generate plant ID
    existing = ["basil_001", "basil_002", "tomato_001"]
    assert generate_plant_id("basil", existing) == "basil_003"
    assert generate_plant_id("tomato", existing) == "tomato_002"
    assert generate_plant_id("strawberry", existing) == "strawberry_001"
    print("✓ Plant ID generation working")

    print()
    print("=" * 65)
    print("✅ All validation tests passed! (VERSION 13.1)")
    print("=" * 65)