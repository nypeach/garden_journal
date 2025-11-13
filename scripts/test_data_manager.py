"""
Test script for data_manager.py
VERSION: 1.0
Tests all data_manager functions with detailed output
"""

import sys
from pathlib import Path
import shutil
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from data_manager import (
    load_data,
    save_data,
    add_plant,
    update_plant_summary,
    move_plant,
    add_daily_entry,
    add_plant_observation,
    get_plant_by_id,
    get_entry_by_date,
    get_all_plants,
    get_all_entries,
    DATA_FILE
)

def print_header(text):
    """Print a formatted header."""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)

def print_step(text):
    """Print a formatted step."""
    print(f"\n→ {text}")

def print_success(text):
    """Print a success message."""
    print(f"  ✓ {text}")

def print_info(text):
    """Print an info message."""
    print(f"  • {text}")

def print_before_after(label, before, after):
    """Print before/after comparison."""
    print(f"  📊 {label}:")
    print(f"     BEFORE: {before}")
    print(f"     AFTER:  {after}")

def print_error(text):
    """Print an error message."""
    print(f"  ✗ ERROR: {text}")

def create_test_backup():
    """Create a backup of current garden_data.json before testing."""
    if DATA_FILE.exists():
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = DATA_FILE.parent / f"garden_data.TEST_BACKUP_{timestamp}.json"
        shutil.copy2(DATA_FILE, backup_file)
        print_success(f"Created test backup: {backup_file.name}")
        return backup_file
    return None

def test_load_data():
    """Test loading garden data."""
    print_header("TEST 1: Load Data")

    try:
        print_step("Loading garden_data.json...")
        data = load_data()

        print_success("Data loaded successfully")
        print_info(f"Found {len(data['plants'])} plants")
        print_info(f"Found {len(data['daily_entries'])} daily entries")

        # Show first few plants
        print_info("Sample plants:")
        for i, plant in enumerate(data['plants'][:3]):
            print(f"       - {plant['plant_id']}: {plant['common_name']}")

        return True
    except Exception as e:
        print_error(str(e))
        return False

def test_add_plant():
    """Test adding a new plant."""
    print_header("TEST 2: Add New Plant")

    try:
        # Get before count
        data_before = load_data()
        plants_before = len(data_before['plants'])

        print_step("Adding test plant: test_basil_999...")
        print_before_after("Plant count", plants_before, "?")

        add_plant(
            plant_id="test_basil_999",
            plant_type="basil",
            common_name="Test Basil",
            variety="Sweet Basil Test",
            purchase_date="20251113",
            location="Panel 5",
            container_type="pot",
            container_name="Test Pot",
            stake_number=None,
            position=None,
            summary="This is a test plant for validation."
        )

        print_success("Plant added successfully")

        # Verify it was added
        print_step("Verifying plant was added...")
        plant = get_plant_by_id("test_basil_999")
        data_after = load_data()
        plants_after = len(data_after['plants'])

        if plant:
            print_success("Plant found in data")
            print_before_after("Plant count", plants_before, plants_after)
            print_info(f"Common name: {plant['common_name']}")
            print_info(f"Location: {plant['current_location']['location']}")
            print_info(f"Summary: {plant['summary']}")
        else:
            print_error("Plant not found after adding")
            return False

        return True
    except Exception as e:
        print_error(str(e))
        return False

def test_update_plant_summary():
    """Test updating plant summary."""
    print_header("TEST 3: Update Plant Summary")

    try:
        # Get before summary
        plant_before = get_plant_by_id("test_basil_999")
        summary_before = plant_before['summary']

        print_step("Updating summary for test_basil_999...")

        new_summary = "Updated test summary with new observations. Plant is thriving!"
        print_before_after("Summary",
                          summary_before[:50] + "..." if len(summary_before) > 50 else summary_before,
                          new_summary[:50] + "..." if len(new_summary) > 50 else new_summary)

        update_plant_summary("test_basil_999", new_summary)

        print_success("Summary updated successfully")

        # Verify update
        print_step("Verifying summary was updated...")
        plant = get_plant_by_id("test_basil_999")
        if plant and plant['summary'] == new_summary:
            print_success("Summary matches new value")
            print_info(f"Full summary: {plant['summary']}")
        else:
            print_error("Summary was not updated correctly")
            return False

        return True
    except Exception as e:
        print_error(str(e))
        return False

def test_move_plant():
    """Test moving a plant."""
    print_header("TEST 4: Move Plant")

    try:
        # Get before location
        plant_before = get_plant_by_id("test_basil_999")
        location_before = plant_before['current_location']['location']
        history_count_before = len(plant_before['location_history'])

        print_step("Moving test_basil_999 from Panel 5 to Panel 10...")
        print_before_after("Current location", location_before, "Panel 10")
        print_before_after("Location history count", history_count_before, "?")

        move_plant(
            plant_id="test_basil_999",
            date="20251113",
            new_location="Panel 10",
            container_type="pot",
            container_name="Test Pot",
            reason="Testing move functionality"
        )

        print_success("Plant moved successfully")

        # Verify move
        print_step("Verifying plant location...")
        plant = get_plant_by_id("test_basil_999")
        if plant:
            current_loc = plant['current_location']['location']
            history_count = len(plant['location_history'])

            if current_loc == "Panel 10":
                print_success(f"Current location updated to: {current_loc}")
                print_before_after("Location history count", history_count_before, history_count)

                # Show last history entry
                last_entry = plant['location_history'][-1]
                print_info(f"Last move: {last_entry['location']} - {last_entry['reason']}")
            else:
                print_error(f"Location not updated correctly: {current_loc}")
                return False
        else:
            print_error("Plant not found")
            return False

        return True
    except Exception as e:
        print_error(str(e))
        return False

def test_add_daily_entry():
    """Test adding a daily entry."""
    print_header("TEST 5: Add Daily Entry")

    try:
        # Get before count
        data_before = load_data()
        entries_before = len(data_before['daily_entries'])

        print_step("Adding daily entry for 20251113...")
        print_before_after("Daily entries count", entries_before, "?")

        add_daily_entry(
            date="20251113",
            summary_of_activities=[
                "Tested data_manager.py functions",
                "Added test plant",
                "Moved test plant"
            ],
            weather={
                "temp_high": 78,
                "temp_low": 68,
                "conditions": "Sunny and clear",
                "sunrise": "0645",
                "sunset": "1745"
            },
            general_observations="Testing day - all systems working well.",
            general_qa=[
                {
                    "question": "How is the data_manager performing?",
                    "answer": "Excellent! All functions working as expected."
                }
            ],
            upcoming_actions=[
                "Build interactive scripts",
                "Start fresh data entry"
            ],
            plant_observations=[]
        )

        print_success("Daily entry added successfully")

        # Verify entry
        print_step("Verifying daily entry...")
        entry = get_entry_by_date("20251113")
        data_after = load_data()
        entries_after = len(data_after['daily_entries'])

        if entry:
            print_success("Entry found in data")
            print_before_after("Daily entries count", entries_before, entries_after)
            print_info(f"Activities: {len(entry['summary_of_activities'])} recorded")
            print_info(f"Weather: {entry['weather']['conditions']}")
            print_info(f"High: {entry['weather']['temp_high']}°F")
        else:
            print_error("Entry not found after adding")
            return False

        return True
    except Exception as e:
        print_error(str(e))
        return False

def test_add_plant_observation():
    """Test adding plant observation to existing entry."""
    print_header("TEST 6: Add Plant Observation")

    try:
        # Get before count
        entry_before = get_entry_by_date("20251113")
        obs_before = len(entry_before['plant_observations'])

        print_step("Adding observation for test_basil_999 to today's entry...")
        print_before_after("Plant observations count", obs_before, "?")

        add_plant_observation(
            date="20251113",
            plant_id="test_basil_999",
            time="1430",
            observation_text="Test observation: Plant looking healthy after move.",
            photos=[
                {
                    "filename": "test_basil_999_20251113_1430_1.jpg",
                    "tag": "after_move",
                    "caption": "Test photo after moving to Panel 10"
                }
            ],
            soil_moisture="lightly moist",
            care_actions=[
                {
                    "action_type": "watering",
                    "amount": "1 cup",
                    "notes": "Light watering after move"
                }
            ],
            plant_qa=[
                {
                    "question": "How did the plant handle the move?",
                    "answer": "Very well! No signs of stress."
                }
            ]
        )

        print_success("Plant observation added successfully")

        # Verify observation
        print_step("Verifying plant observation...")
        entry = get_entry_by_date("20251113")
        obs_after = len(entry['plant_observations'])

        if entry and len(entry['plant_observations']) > 0:
            obs = entry['plant_observations'][0]
            print_success(f"Found observation for {obs['plant_id']}")
            print_before_after("Plant observations count", obs_before, obs_after)
            print_info(f"Time: {obs['time']}")
            print_info(f"Observation: {obs['observation']}")
            print_info(f"Photos: {len(obs['photos'])}")
            print_info(f"Care actions: {len(obs['care_actions'])}")
        else:
            print_error("Observation not found after adding")
            return False

        return True
    except Exception as e:
        print_error(str(e))
        return False

def test_get_all_functions():
    """Test get_all functions."""
    print_header("TEST 7: Get All Functions")

    try:
        print_step("Testing get_all_plants()...")
        plants = get_all_plants()
        print_success(f"Retrieved {len(plants)} plants")

        print_step("Testing get_all_entries()...")
        entries = get_all_entries()
        print_success(f"Retrieved {len(entries)} daily entries")

        # Show date range
        if entries:
            dates = [e['date'] for e in entries]
            print_info(f"Date range: {min(dates)} to {max(dates)}")

        return True
    except Exception as e:
        print_error(str(e))
        return False

def test_validation_errors():
    """Test that validation catches errors."""
    print_header("TEST 8: Validation Error Handling")

    tests_passed = 0
    tests_total = 3

    # Test 1: Invalid plant ID format
    print_step("Testing invalid plant ID format...")
    try:
        add_plant(
            plant_id="invalid-id-format",
            plant_type="basil",
            common_name="Invalid Plant",
            variety=None,
            purchase_date="20251113",
            location="Panel 1",
            container_type="pot",
            container_name="Test"
        )
        print_error("Should have rejected invalid plant ID format")
    except ValueError as e:
        print_success(f"Correctly rejected invalid ID: {str(e)}")
        tests_passed += 1

    # Test 2: Invalid date format
    print_step("Testing invalid date format...")
    try:
        add_plant(
            plant_id="test_003",
            plant_type="basil",
            common_name="Test",
            variety=None,
            purchase_date="20251332",  # Invalid day (32)
            location="Panel 1",
            container_type="pot",
            container_name="Test"
        )
        print_error("Should have rejected invalid date format")
    except ValueError as e:
        print_success(f"Correctly rejected invalid date: {str(e)}")
        tests_passed += 1

    # Test 3: Duplicate plant ID
    print_step("Testing duplicate plant ID...")
    try:
        add_plant(
            plant_id="test_basil_999",  # Already exists
            plant_type="basil",
            common_name="Duplicate",
            variety=None,
            purchase_date="20251113",
            location="Panel 1",
            container_type="pot",
            container_name="Test"
        )
        print_error("Should have rejected duplicate plant ID")
    except ValueError as e:
        print_success(f"Correctly rejected duplicate ID: {str(e)}")
        tests_passed += 1

    print_info(f"Validation tests passed: {tests_passed}/{tests_total}")
    return tests_passed == tests_total

def cleanup_test_data():
    """Remove test plant and entry from data if they exist."""
    try:
        data = load_data()

        # Remove test plants
        original_count = len(data["plants"])
        data["plants"] = [p for p in data["plants"] if not p["plant_id"].startswith("test_")]
        removed_plants = original_count - len(data["plants"])

        # Remove test entry
        original_entries = len(data["daily_entries"])
        data["daily_entries"] = [e for e in data["daily_entries"] if e["date"] != "20251113"]
        removed_entries = original_entries - len(data["daily_entries"])

        if removed_plants > 0 or removed_entries > 0:
            save_data(data, create_backup=False)
            return removed_plants, removed_entries

        return 0, 0
    except Exception as e:
        print_error(f"Cleanup error: {str(e)}")
        return 0, 0

def main():
    """Run all tests."""
    print("\n" + "=" * 70)
    print("  GARDEN JOURNAL DATA MANAGER TEST SUITE")
    print("  VERSION: 1.0")
    print("=" * 70)

    # Clean up any leftover test data from previous runs
    print_step("Cleaning up any previous test data...")
    removed_plants, removed_entries = cleanup_test_data()
    if removed_plants > 0 or removed_entries > 0:
        print_success(f"Removed {removed_plants} test plant(s) and {removed_entries} test entry(ies)")
    else:
        print_info("No previous test data found")

    # Create backup before testing
    print_step("Creating backup before tests...")
    backup_file = create_test_backup()

    # Run all tests
    results = []
    results.append(("Load Data", test_load_data()))
    results.append(("Add Plant", test_add_plant()))
    results.append(("Update Summary", test_update_plant_summary()))
    results.append(("Move Plant", test_move_plant()))
    results.append(("Add Daily Entry", test_add_daily_entry()))
    results.append(("Add Plant Observation", test_add_plant_observation()))
    results.append(("Get All Functions", test_get_all_functions()))
    results.append(("Validation Errors", test_validation_errors()))

    # Print summary
    print_header("TEST SUMMARY")

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"  {status}: {test_name}")

    print(f"\n  Overall: {passed}/{total} tests passed")

    if backup_file:
        print(f"\n  Test backup saved at: {backup_file.name}")
        print(f"  Original data preserved - test data remains in garden_data.json")

    print("\n" + "=" * 70)

    if passed == total:
        print("  ✓ ALL TESTS PASSED!")
        print("  You can inspect the test data added to garden_data.json")
    else:
        print("  ✗ SOME TESTS FAILED - Check output above")

    print("=" * 70 + "\n")

if __name__ == "__main__":
    main()