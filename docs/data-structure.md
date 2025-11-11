# Garden Journal Data Structure

## Overview

The garden journal uses a single JSON file (`data/garden_data.json`) to store all garden data. This document describes the complete schema.

## File Location

```
data/garden_data.json
```

## Root Structure

```json
{
  "metadata": { },
  "plants": [ ],
  "locations": { },
  "daily_entries": [ ]
}
```

---

## Metadata

Information about the garden itself.

```json
{
  "metadata": {
    "garden_name": "Jodi's Garden Journal",
    "start_date": "2025-10-08",
    "location": "Miami, Florida",
    "garden_type": "Container/Fence Panel Garden",
    "last_updated": "2025-11-11"
  }
}
```

### Fields

- `garden_name` (string) - Display name for your garden
- `start_date` (string) - Date garden started (YYYYMMDD)
- `location` (string) - Geographic location
- `garden_type` (string) - Type of garden setup
- `last_updated` (string) - Last modification date

---

## Plants Array

Each plant in your garden. **Plants are the primary entity** - locations are tracked as history.

### Plant Object Structure

```json
{
  "plant_id": "basil_001",
  "common_name": "Basil - Left",
  "variety": "Sweet Basil",
  "purchase_date": "20251008",
  "source": "Local Nursery",
  "status": "active",

  "location_history": [
    {
      "date": "20251008",
      "location": "Picnic Table",
      "container": "8\" white round pot, 0.94 gal",
      "soil_mix": "Miracle-Gro Moisture Control",
      "reason": "Initial purchase, observation period"
    }
  ],

  "current_location": {
    "location": "Panel 1",
    "container": "8\" white round pot, 0.94 gal",
    "soil_mix": "Miracle-Gro Moisture Control"
  }
}
```

For complete field definitions, see the full documentation in the repository.

---

## Daily Entries Array

Records of daily observations and activities.

See `data/garden_data.example.json` for a complete working example.

---

## See Also

- [Photo Naming Convention](photo-naming.md)
- [Daily Workflow](workflow.md)
- [Setup Instructions](setup.md)
