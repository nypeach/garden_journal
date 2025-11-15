"""
Garden Journal Data Manager
VERSION: 1.0
Handles all JSON read/write operations for garden_data.json

Note: plants is stored as an array, not a dict
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List
import shutil

from schema import (
    validate_plant_id,
    validate_date,
    validate_time,
    validate_plant_status,
    validate_action_type
)


# Path constants
DATA_DIR = Path(__file__).parent.parent / "data"
DATA_FILE = DATA_DIR / "garden_data.json"
BACKUP_DIR = DATA_DIR / "backups"


def _ensure_backup_dir():
    """Create backups directory if it doesn't exist."""
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)


def load_data() -> Dict[str, Any]:
    """
    Load garden_data.json with validation.

    Returns:
        Dict containing garden data

    Raises:
        FileNotFoundError: If garden_data.json doesn't exist
        json.JSONDecodeError: If JSON is malformed
        ValueError: If data fails validation
    """
    if not DATA_FILE.exists():
        raise FileNotFoundError(f"Data file not found: {DATA_FILE}")

    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Validate structure
    if "plants" not in data:
        raise ValueError("Missing 'plants' key in data")
    if not isinstance(data["plants"], list):
        raise ValueError("'plants' must be an array/list")
    if "daily_entries" not in data:
        raise ValueError("Missing 'daily_entries' key in data")

    # Basic validation - check plant IDs
    for plant in data["plants"]:
        if "plant_id" not in plant:
            raise ValueError(f"Plant missing 'plant_id' field")
        if not validate_plant_id(plant["plant_id"]):
            raise ValueError(f"Invalid plant_id format: {plant['plant_id']}")

    # Basic validation - check entry dates
    for entry in data["daily_entries"]:
        if "date" not in entry:
            raise ValueError("Daily entry missing 'date' field")
        if not validate_date(entry["date"]):
            raise ValueError(f"Invalid date format: {entry['date']}")

    return data


def save_data(data: Dict[str, Any], create_backup: bool = True) -> None:
    """
    Save garden_data.json with optional timestamped backup.

    Args:
        data: Garden data to save
        create_backup: If True, create timestamped backup before saving

    Raises:
        ValueError: If data fails validation
    """
    # Validate before saving
    if "plants" not in data:
        raise ValueError("Missing 'plants' key in data")
    if not isinstance(data["plants"], list):
        raise ValueError("'plants' must be an array/list")
    if "daily_entries" not in data:
        raise ValueError("Missing 'daily_entries' key in data")

    # Basic validation - check plant IDs
    for plant in data["plants"]:
        if "plant_id" not in plant:
            raise ValueError(f"Plant missing 'plant_id' field")
        if not validate_plant_id(plant["plant_id"]):
            raise ValueError(f"Invalid plant_id format: {plant['plant_id']}")

    # Basic validation - check entry dates
    for entry in data["daily_entries"]:
        if "date" not in entry:
            raise ValueError("Daily entry missing 'date' field")
        if not validate_date(entry["date"]):
            raise ValueError(f"Invalid date format: {entry['date']}")

    # Create backup if requested and file exists
    if create_backup and DATA_FILE.exists():
        _ensure_backup_dir()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = BACKUP_DIR / f"garden_data.backup.{timestamp}.json"
        shutil.copy2(DATA_FILE, backup_file)
        print(f"Backup created: {backup_file}")

    # Save data
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"Data saved: {DATA_FILE}")


def add_plant(
    plant_id: str,
    plant_type: str,
    common_name: str,
    variety: Optional[str],
    purchase_date: str,
    location: str,
    container_type: str,
    container_name: str,
    soil_mix: str,
    stake_number: Optional[int] = None,
    position: Optional[str] = None,
    summary: str = ""
) -> None:
    """
    Add a new plant with initial location.

    Args:
        plant_id: Unique plant ID (e.g., 'basil_001')
        plant_type: Type of plant (e.g., 'basil', 'tomato')
        common_name: Display name (e.g., 'Basil - Left')
        variety: Plant variety (optional)
        purchase_date: Date in YYYYMMDD format
        location: Initial location (e.g., 'Panel 1', 'Picnic Table')
        container_type: Type of container (e.g., 'pot', 'raised_bed')
        container_name: Name of container (e.g., 'Basil Pot - Left')
        stake_number: Stake number for staked containers (optional)
        position: Position description for shared containers (optional)
        summary: Initial plant summary/notes (optional)

    Raises:
        ValueError: If plant_id already exists or validation fails
    """
    validate_plant_id(plant_id)
    validate_date(purchase_date)

    data = load_data()

    # Check if plant_id already exists
    for plant in data["plants"]:
        if plant["plant_id"] == plant_id:
            raise ValueError(f"Plant ID already exists: {plant_id}")

    # Create new plant record
    new_plant = {
        "plant_id": plant_id,
        "plant_type": plant_type,
        "common_name": common_name,
        "variety": variety,
        "purchase_date": purchase_date,
        "status": "active",
        "current_location": {
            "location": location,
            "container_type": container_type,
            "container_name": container_name,
            "soil_mix": soil_mix,
            "stake_number": stake_number,
            "position": position
        },
        "location_history": [
            {
                "date": purchase_date,
                "location": location,
                "container_type": container_type,
                "container_name": container_name,
                "soil_mix": soil_mix,
                "stake_number": stake_number,
                "position": position,
                "reason": "Initial placement"
            }
        ],
        "summary": summary
    }

    # Add to data
    data["plants"].append(new_plant)

    # Save
    save_data(data)
    print(f"Added plant: {plant_id} ({common_name})")


def update_plant_summary(plant_id: str, summary: str) -> None:
    """
    Update plant summary field.

    Args:
        plant_id: Plant ID to update
        summary: New summary text

    Raises:
        ValueError: If plant not found
    """
    validate_plant_id(plant_id)

    data = load_data()

    # Find the plant
    plant = None
    for p in data["plants"]:
        if p["plant_id"] == plant_id:
            plant = p
            break

    if plant is None:
        raise ValueError(f"Plant not found: {plant_id}")

    plant["summary"] = summary

    save_data(data)
    print(f"Updated summary for: {plant_id}")


def move_plant(
    plant_id: str,
    date: str,
    new_location: str,
    container_type: str,
    container_name: str,
    reason: str,
    stake_number: Optional[int] = None,
    position: Optional[str] = None
) -> None:
    """
    Move plant to new location, updating location history and current location.

    Args:
        plant_id: Plant ID to move
        date: Move date in YYYYMMDD format
        new_location: New location (e.g., 'Panel 5')
        container_type: Container type at new location
        container_name: Container name at new location
        reason: Reason for move
        stake_number: Stake number if applicable (optional)
        position: Position description if applicable (optional)

    Raises:
        ValueError: If plant not found or validation fails
    """
    validate_plant_id(plant_id)
    validate_date(date)

    data = load_data()

    # Find the plant
    plant = None
    for p in data["plants"]:
        if p["plant_id"] == plant_id:
            plant = p
            break

    if plant is None:
        raise ValueError(f"Plant not found: {plant_id}")

    # Add to location history
    location_entry = {
        "date": date,
        "location": new_location,
        "container_type": container_type,
        "container_name": container_name,
        "stake_number": stake_number,
        "position": position,
        "reason": reason
    }

    plant["location_history"].append(location_entry)

    # Update current location
    plant["current_location"] = {
        "location": new_location,
        "container_type": container_type,
        "container_name": container_name,
        "stake_number": stake_number,
        "position": position
    }

    save_data(data)
    print(f"Moved {plant_id} to {new_location}")


def add_daily_entry(
    date: str,
    summary_of_activities: List[str],
    weather: Dict[str, Any],
    general_observations: Optional[str] = None,
    general_qa: Optional[List[Dict[str, str]]] = None,
    upcoming_actions: Optional[List[str]] = None,
    plant_observations: Optional[List[Dict[str, Any]]] = None
) -> None:
    """
    Add a complete daily entry.

    Args:
        date: Entry date in YYYYMMDD format
        summary_of_activities: List of activity strings
        weather: Weather dict with temp_high, temp_low, conditions, etc.
        general_observations: General garden observations (optional)
        general_qa: List of Q&A dicts (optional)
        upcoming_actions: List of planned actions (optional)
        plant_observations: List of plant observation dicts (optional)

    Raises:
        ValueError: If entry for date already exists or validation fails
    """
    validate_date(date)

    data = load_data()

    # Check if entry already exists
    for entry in data["daily_entries"]:
        if entry["date"] == date:
            raise ValueError(f"Daily entry already exists for date: {date}")

    # Create new entry
    new_entry = {
        "date": date,
        "summary_of_activities": summary_of_activities,
        "weather": weather,
        "general_observations": general_observations,
        "general_qa": general_qa or [],
        "upcoming_actions": upcoming_actions or [],
        "plant_observations": plant_observations or []
    }

    # Add and sort by date (most recent first)
    data["daily_entries"].append(new_entry)
    data["daily_entries"].sort(key=lambda x: x["date"], reverse=True)

    save_data(data)
    print(f"Added daily entry for: {date}")


def add_plant_observation(
    date: str,
    plant_id: str,
    time: str,
    observation_text: str,
    photos: Optional[List[Dict[str, Any]]] = None,
    soil_moisture: Optional[str] = None,
    care_actions: Optional[List[Dict[str, Any]]] = None,
    plant_qa: Optional[List[Dict[str, str]]] = None,
    temporary_location: Optional[Dict[str, str]] = None
) -> None:
    """
    Add a plant observation to an existing daily entry.

    Args:
        date: Entry date in YYYYMMDD format
        plant_id: Plant ID for observation
        time: Time in HHMM format
        observation_text: Observation description
        photos: List of photo dicts (optional)
        soil_moisture: Soil moisture description (optional)
        care_actions: List of care action dicts (optional)
        plant_qa: List of Q&A dicts specific to plant (optional)
        temporary_location: Temporary location dict (optional)

    Raises:
        ValueError: If entry not found, plant not found, or validation fails
    """
    validate_date(date)
    validate_plant_id(plant_id)
    validate_time(time)

    data = load_data()

    # Verify plant exists
    plant_exists = False
    for plant in data["plants"]:
        if plant["plant_id"] == plant_id:
            plant_exists = True
            break

    if not plant_exists:
        raise ValueError(f"Plant not found: {plant_id}")

    # Find the daily entry
    entry = None
    for e in data["daily_entries"]:
        if e["date"] == date:
            entry = e
            break

    if entry is None:
        raise ValueError(f"Daily entry not found for date: {date}")

    # Create observation
    observation = {
        "plant_id": plant_id,
        "time": time,
        "observation": observation_text,
        "photos": photos or [],
        "soil_moisture": soil_moisture,
        "care_actions": care_actions or [],
        "plant_qa": plant_qa or [],
        "temporary_location": temporary_location
    }

    # Add to entry
    entry["plant_observations"].append(observation)

    # Sort observations by time
    entry["plant_observations"].sort(key=lambda x: x["time"])

    save_data(data)
    print(f"Added observation for {plant_id} at {time}")


def get_plant_by_id(plant_id: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve plant data by ID.

    Args:
        plant_id: Plant ID to retrieve

    Returns:
        Plant data dict or None if not found
    """
    validate_plant_id(plant_id)

    data = load_data()

    for plant in data["plants"]:
        if plant["plant_id"] == plant_id:
            return plant

    return None


def get_entry_by_date(date: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve daily entry by date.

    Args:
        date: Date in YYYYMMDD format

    Returns:
        Daily entry dict or None if not found
    """
    validate_date(date)

    data = load_data()

    for entry in data["daily_entries"]:
        if entry["date"] == date:
            return entry

    return None


def get_all_plants() -> List[Dict[str, Any]]:
    """
    Retrieve all plants.

    Returns:
        List of all plants
    """
    data = load_data()
    return data["plants"]


def get_all_entries() -> List[Dict[str, Any]]:
    """
    Retrieve all daily entries.

    Returns:
        List of all daily entries sorted by date (most recent first)
    """
    data = load_data()
    return data["daily_entries"]