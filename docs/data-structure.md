# Garden Journal Data Structure

**VERSION: 13**
**Last Updated: 2025-11-11**

---

## Overview

The garden journal uses a single JSON file (`data/garden_data.json`) to store all garden data. Version 13 introduces comprehensive tracking for multiple daily observations, detailed actions, photo metadata, and temporary location changes.

## File Location

```
data/garden_data.json
```

## Root Structure

```json
{
  "_schema_version": "13",
  "_last_updated": "2025-11-11",
  "metadata": { },
  "plants": [ ],
  "locations": { },
  "daily_entries": [ ]
}
```

---

## What's New in Version 13

### Major Enhancements

1. **Multiple observations per plant per day** - Track morning, afternoon, and evening checks separately
2. **Photo metadata system** - Tag photos as before/after, add captions, link to specific observations
3. **Detailed action tracking** - Record amounts (cups, oz), products (Captain Jack's), methods (spray, hose)
4. **Soil moisture descriptions** - "bone dry", "lightly moist", "very dry 1 inch down"
5. **Temporary location tracking** - When plants go indoors, get covered, or move temporarily
6. **Position in shared containers** - "left section", "edges", "center" for multi-plant containers
7. **Upcoming actions** - Plan future tasks with target dates
8. **Product/brand tracking** - Know exactly what you used
9. **Container naming** - Group plants by container name (Pepper Box, Garlic Box, etc.)
10. **Stake support** - Full support for staked containers (Pepper Box with 3 stakes, Raised Bed with 4)

---

## Metadata

Basic information about your garden.

```json
{
  "metadata": {
    "garden_name": "Jodi's Garden Journal",
    "start_date": "20251008",
    "location": "Miami, Florida",
    "garden_type": "Container/Fence Panel Garden"
  }
}
```

### Fields

- `garden_name` (string) - Display name for your garden
- `start_date` (string) - Date garden started (YYYYMMDD)
- `location` (string) - Geographic location
- `garden_type` (string) - Type of garden setup

---

## Plants Array

Each plant in your garden with complete history.

### Plant Object Structure

```json
{
  "plant_id": "basil_001",
  "common_name": "Basil - Left",
  "variety": "Sweet Basil",
  "purchase_date": "20251008",
  "source": "Lowe's",
  "status": "active",

  "location_history": [ ],
  "current_location": { },
  "temporary_locations": [ ],
  "care_history": [ ],
  "growth_stages": [ ]
}
```

### Required Fields

- `plant_id` (string) - Unique identifier: `{planttype}_{###}` (e.g., "basil_001")
- `common_name` (string) - Display name (e.g., "Basil - Left")
- `purchase_date` (string) - Date acquired (YYYYMMDD)
- `status` (string) - "active", "removed", "died", "harvested"
- `location_history` (array) - Complete movement history
- `current_location` (object) - Current state

### Optional Fields

- `variety` (string) - Plant variety (e.g., "Sweet Basil", "Husky Cherry Red")
- `source` (string) - Where acquired (e.g., "Lowe's", "Garden Center")
- `temporary_locations` (array) - Temporary moves (indoors, covered, etc.)
- `care_history` (array) - All care actions
- `growth_stages` (array) - Growth milestones

---

## Location History

**NEW IN V13:** Added `container_name`, `stake`, and `position` fields

Tracks every location change for a plant, including moves between:
- Physical locations (Picnic Table → Panel 14 → Panel 1)
- Containers (transplanting to larger pots)
- Stakes (moving within raised bed)

```json
{
  "location_history": [
    {
      "date": "20251008",
      "location": "Picnic Table",
      "container_name": "Basil Pot - Left",
      "container_type": "8\" white round pot, 0.94 gal",
      "stake": null,
      "position": null,
      "soil_mix": "Original nursery potting mix",
      "reason": "Initial purchase"
    },
    {
      "date": "20251020",
      "location": "Panel 1",
      "container_name": "Basil Pot - Left",
      "container_type": "8\" white round pot, 0.94 gal",
      "stake": null,
      "position": null,
      "soil_mix": "Original nursery potting mix",
      "reason": "Moved to first morning sun position"
    }
  ]
}
```

### Fields

- `date` (string) - Date of move (YYYYMMDD)
- `location` (string) - Physical location (Picnic Table, Panel 1, Indoors, etc.)
- `container_name` (string) - **NEW** Friendly container name for grouping
- `container_type` (string) - Technical description with dimensions
- `stake` (integer or null) - **NEW** Stake number if applicable (1, 2, 3, 4)
- `position` (string or null) - **NEW** Position in shared container ("left section", "edges", "center")
- `soil_mix` (string) - Soil composition
- `reason` (string) - Why moved
- `transplant_method` (string, optional) - Special notes (e.g., "Sideways planting")

---

## Temporary Locations

**NEW IN V13**

Track when plants are temporarily moved for protection, then returned.

```json
{
  "temporary_locations": [
    {
      "date": "20251110",
      "time": "1800",
      "temp_location": "Indoors",
      "reason": "Cold protection - temps below 40°F",
      "returned_date": "20251111",
      "returned_time": "0900"
    },
    {
      "date": "20251110",
      "time": "1800",
      "temp_location": "Covered with plastic tablecloth",
      "reason": "Cold protection overnight",
      "returned_date": "20251111",
      "returned_time": "0800"
    }
  ]
}
```

### Fields

- `date` (string) - Date moved temporarily (YYYYMMDD)
- `time` (string) - Time moved (HHMM)
- `temp_location` (string) - Where it went ("Indoors", "Covered with blanket", "Garage")
- `reason` (string) - Why moved
- `returned_date` (string, optional) - When returned to normal location
- `returned_time` (string, optional) - Time returned

---

## Care History

**ENHANCED IN V13**

Detailed tracking of every action taken on a plant.

```json
{
  "care_history": [
    {
      "date": "20251111",
      "time": "1400",
      "action_type": "watering",
      "details": "Watered after being brought back outside from cold night",
      "amount": "1½ cups",
      "product": null,
      "method": "Slowly and evenly over soil surface",
      "notes": "Soil was very dry, plant was indoors overnight"
    },
    {
      "date": "20251111",
      "time": "1500",
      "action_type": "pruning",
      "details": "Removed all lower speckled branches",
      "amount": "Multiple branches",
      "product": null,
      "method": "Clean scissors, cut at main stem",
      "notes": "Early blight on lower leaves, no fruit on removed branches"
    },
    {
      "date": "20251111",
      "time": "1520",
      "action_type": "mulching",
      "details": "Added organic mulch layer",
      "amount": "1-1.5 inch layer",
      "product": "Miracle-Gro Organic Choice",
      "method": "Around base, not touching stem",
      "notes": "To retain moisture and prevent soil splash"
    },
    {
      "date": "20251111",
      "time": "1445",
      "action_type": "treatment",
      "details": "Applied neem oil spray",
      "amount": "Light mist",
      "product": "Captain Jack's Neem Oil",
      "method": "Spray on tops and undersides of leaves",
      "notes": "First neem treatment for this plant"
    }
  ]
}
```

### Fields

- `date` (string) - YYYYMMDD
- `time` (string) - **NEW** HHMM - exact time action was taken
- `action_type` (string) - Type of action (see valid types below)
- `details` (string) - Description of what was done
- `amount` (string, optional) - **NEW** Quantity ("1½ cups", "16 oz", "½ cup")
- `product` (string, optional) - **NEW** Brand/product name
- `method` (string, optional) - **NEW** How it was done
- `notes` (string, optional) - Additional context

### Valid Action Types

- `watering` - Any watering activity
- `pruning` - Removing leaves, branches, flowers
- `treatment` - Neem oil, fungicides, pest control
- `feeding` - Fertilizer application
- `mulching` - Adding mulch
- `transplanting` - Moving to new container
- `seeding` - Planting seeds
- `thinning` - Removing excess seedlings
- `staking` - Adding stakes or support
- `covering` - Adding frost protection
- `observation` - Just observing, no action
- `moving` - Changing location
- `soil_amendment` - Adding soil, compost, etc.
- `pest_control` - Hand-picking pests, barriers

---

## Daily Entries

**SIGNIFICANTLY ENHANCED IN V13**

### Daily Entry Structure

```json
{
  "date": "20251111",
  "time_of_entry": "1400",

  "weather": { },
  "activities": [ ],
  "observations": [ ],
  "questions_and_answers": [ ],
  "upcoming_actions": [ ],
  "plant_observations": [ ]
}
```

---

### Weather

Same as before, tracks conditions for the day.

```json
{
  "weather": {
    "temp_high": 68,
    "temp_low": 40,
    "conditions": "Sunny and clear",
    "sunrise": "0653",
    "sunset": "1745",
    "humidity": null,
    "wind": "Light breeze",
    "notes": "Cold night, brought several plants indoors"
  }
}
```

---

### Activities (Garden-Wide)

Simple array of strings describing what you did that day.

```json
{
  "activities": [
    "Brought basil and strawberry plants back outside after cold night indoors",
    "Watered multiple plants that were dry from overnight",
    "Pruned tomato plant - removed diseased lower branches",
    "Added mulch to tomato plant",
    "Applied neem oil to several plants"
  ]
}
```

---

### Observations (Garden-Wide)

General notes not specific to one plant.

```json
{
  "observations": [
    "All plants survived the cold night well",
    "Tomato plant has first fruits forming!",
    "Some fungal leaf spot issues on strawberry and tomato",
    "Arugula showing excellent recovery after reseeding"
  ]
}
```

---

### Upcoming Actions

**NEW IN V13**

Plan future tasks with optional target dates.

```json
{
  "upcoming_actions": [
    {
      "description": "Apply Captain Jack's neem oil to Strawberry - Right",
      "target_date": "20251112",
      "target_timeframe": "tomorrow morning",
      "plants_affected": ["strawberry_002"]
    },
    {
      "description": "Add potting mix layer and reseed chives",
      "target_date": null,
      "target_timeframe": "in a few days",
      "plants_affected": ["broccoli_001", "chives_001"]
    }
  ]
}
```

### Fields

- `description` (string) - What needs to be done
- `target_date` (string or null) - Specific date if known (YYYYMMDD)
- `target_timeframe` (string or null) - Relative timeframe ("tomorrow", "in a few days")
- `plants_affected` (array) - List of plant_ids this affects

---

### Plant Observations

**SIGNIFICANTLY ENHANCED IN V13**

Each observation now includes:
- Exact timestamp
- Soil moisture description
- Detailed actions with amounts/products
- Photo metadata with tags

```json
{
  "plant_observations": [
    {
      "plant_id": "tomato_001",
      "time": "1500",
      "location": "Raised Bed - Panels 16-18",
      "container_name": "Raised Bed",
      "container_type": "2' x 6' x 10\" raised bed",
      "stake": 1,
      "position": null,
      "soil_mix": "Topsoil/Sand mix",
      "soil_moisture": "dry 1 inch down before watering",
      "current_stage": "Fruiting",
      "next_stage": "Fruit development",
      "observations": "Plant vigorous with first fruits forming! Speckled lower leaves show early blight.",
      "actions_taken": [
        "Pruned all lower speckled branches",
        "Deep watered at base",
        "Added 1-1.5\" Miracle-Gro Organic Choice mulch",
        "Watered mulch to settle"
      ],
      "notes": "Plant will fill out again in 1-2 weeks with new side shoots.",
      "plant_qa": {
        "question": "Will it fill out again after I chopped so much off?",
        "answer": "Yes! New side shoots emerge in 5-7 days. Pruning strengthens the main stem."
      },
      "photos": [
        {
          "filename": "tomato_001_20251111_1445_1.jpg",
          "timestamp": "1445",
          "tags": ["before_pruning", "diseased_leaves"],
          "caption": "Before pruning - showing speckled lower leaves"
        },
        {
          "filename": "tomato_001_20251111_1530_1.jpg",
          "timestamp": "1530",
          "tags": ["after_pruning", "after_mulching"],
          "caption": "After pruning and mulching - clean lower stem"
        }
      ]
    }
  ]
}
```

### Plant Observation Fields

#### Required Fields
- `plant_id` (string) - References plant from plants array
- `time` (string) - **NEW** When this observation was made (HHMM)
- `location` (string) - Current location
- `container_name` (string) - **NEW** Container friendly name
- `container_type` (string) - Container description
- `soil_mix` (string) - Soil composition
- `current_stage` (string) - Current growth stage
- `next_stage` (string) - Expected next stage
- `observations` (string) - What you observed

#### Optional Fields
- `stake` (integer or null) - **NEW** Stake number (1, 2, 3, 4)
- `position` (string or null) - **NEW** Position in shared container
- `soil_moisture` (string or null) - **NEW** Moisture description
- `actions_taken` (array) - **NEW** List of actions during this observation
- `notes` (string) - Additional notes
- `plant_qa` (object or null) - Plant-specific Q&A
- `photos` (array) - **NEW** Photo metadata objects

---

## Photo Metadata

**NEW IN V13**

Each photo now has rich metadata for better organization and display.

```json
{
  "filename": "tomato_001_20251111_1445_1.jpg",
  "timestamp": "1445",
  "tags": ["before_pruning", "diseased_leaves"],
  "caption": "Before pruning - showing speckled lower leaves"
}
```

### Fields

- `filename` (string) - Photo filename (follows naming convention)
- `timestamp` (string) - When photo was taken (HHMM)
- `tags` (array) - Descriptive tags for filtering/organizing
- `caption` (string, optional) - Human-readable description

### Common Photo Tags

**Timing:**
- `before_pruning`, `after_pruning`
- `before_watering`, `after_watering`
- `before_treatment`, `after_treatment`
- `morning`, `afternoon`, `evening`

**Content:**
- `full_plant` - Whole plant visible
- `closeup` - Close-up of specific feature
- `soil_condition` - Showing soil state
- `diseased_leaves` - Problem areas
- `healthy_growth` - Good progress
- `fruit_forming` - Fruits/flowers visible
- `chew_marks` - Pest damage
- `new_growth` - Fresh leaves/shoots

---

## Soil Moisture Descriptions

**NEW IN V13**

Standard descriptions for soil moisture levels:

- `"bone dry"` - Completely dry, powdery
- `"very dry"` - Dry throughout
- `"dry 1 inch down"` - Surface dry, moist below
- `"lightly moist"` - Slightly damp
- `"moist"` - Good moisture level
- `"very moist"` - Quite wet but not soggy
- `"soggy"` - Too much water
- `"dry through and through"` - Dry at all levels

---

## Container Names and Grouping

**NEW IN V13**

Container names help group plants that share containers.

### Examples

**Individual Containers:**
- `"Basil Pot - Left"`
- `"Basil Pot - Right"`
- `"Strawberry Pot - Right"`

**Shared Containers with Stakes:**
- `"Pepper Box"` - 3 peppers at stakes 1, 2, 3
- `"Raised Bed"` - Multiple veggies at stakes 1, 2, 3, 4

**Shared Containers with Positions:**
- `"Garlic & Scallion Box"` - Garlic in sections, scallions at edges
- `"Arugula & Cilantro Box"` - Arugula left side, cilantro right side
- `"5-Herb Box"` - 5 herbs in different sections
- `"Broccoli & Chives Box"` - Broccoli center, chives edges

### Display Logic

When generating HTML:

1. **Group by location + container_name**
2. **If multiple plants have same container_name AND stakes:**
   - Display container header once
   - List plants by stake number (like Raised Bed)
3. **If multiple plants have same container_name but NO stakes:**
   - Display container header once
   - List plants with their positions

---

## Complete Examples

### Example 1: Plant with Location History

A basil plant that moved multiple times:

```json
{
  "plant_id": "basil_001",
  "common_name": "Basil - Left",
  "variety": "Sweet Basil",
  "purchase_date": "20251008",
  "source": "Lowe's",
  "status": "active",

  "location_history": [
    {
      "date": "20251008",
      "location": "Picnic Table",
      "container_name": "Basil Pot - Left",
      "container_type": "8\" white round pot, 0.94 gal",
      "stake": null,
      "position": null,
      "soil_mix": "Original nursery potting mix",
      "reason": "Initial purchase"
    },
    {
      "date": "20251015",
      "location": "Panel 14",
      "container_name": "Basil Pot - Left",
      "container_type": "8\" white round pot, 0.94 gal",
      "stake": null,
      "position": null,
      "soil_mix": "Original nursery potting mix",
      "reason": "Testing sun exposure"
    },
    {
      "date": "20251020",
      "location": "Panel 1",
      "container_name": "Basil Pot - Left",
      "container_type": "8\" white round pot, 0.94 gal",
      "stake": null,
      "position": null,
      "soil_mix": "Original nursery potting mix",
      "reason": "Moved to first morning sun position"
    }
  ],

  "temporary_locations": [
    {
      "date": "20251110",
      "time": "1800",
      "temp_location": "Indoors",
      "reason": "Cold protection - temps below 40°F",
      "returned_date": "20251111",
      "returned_time": "0900"
    }
  ]
}
```

### Example 2: Staked Container (Peppers)

Three peppers sharing a window planter with stakes:

```json
{
  "plant_id": "pepper_001",
  "common_name": "Scotch Bonnet",
  "variety": "Scotch Bonnet",
  "current_location": {
    "location": "Panel 7",
    "container_name": "Pepper Box",
    "container_type": "Window planter 23.5\" × 6\" (shared, 3 stakes)",
    "stake": 1,
    "position": null,
    "soil_mix": "Potting mix"
  }
},
{
  "plant_id": "pepper_002",
  "common_name": "Orange Cali Wonder",
  "variety": "California Wonder",
  "current_location": {
    "location": "Panel 7",
    "container_name": "Pepper Box",
    "container_type": "Window planter 23.5\" × 6\" (shared, 3 stakes)",
    "stake": 2,
    "position": null,
    "soil_mix": "Potting mix"
  }
},
{
  "plant_id": "pepper_003",
  "common_name": "Jalapeño",
  "variety": "Jalapeño",
  "current_location": {
    "location": "Panel 7",
    "container_name": "Pepper Box",
    "container_type": "Window planter 23.5\" × 6\" (shared, 3 stakes)",
    "stake": 3,
    "position": null,
    "soil_mix": "Potting mix"
  }
}
```

**Display in HTML:**
```
Panel 7 — Pepper Box
  Stake 1 — Scotch Bonnet
  Stake 2 — Orange Cali Wonder
  Stake 3 — Jalapeño
```

### Example 3: Shared Container with Positions (Garlic)

Multiple plants sharing container, no stakes, using positions:

```json
{
  "plant_id": "garlic_001",
  "common_name": "Siberian Hardneck Garlic",
  "current_location": {
    "location": "Panel 8",
    "container_name": "Garlic & Scallion Box",
    "container_type": "Window planter 23.5\" × 6\" (shared)",
    "stake": null,
    "position": "left section",
    "soil_mix": "Miracle-Gro Moisture Control"
  }
},
{
  "plant_id": "garlic_002",
  "common_name": "Music Hardneck Garlic",
  "current_location": {
    "location": "Panel 8",
    "container_name": "Garlic & Scallion Box",
    "stake": null,
    "position": "center section"
  }
},
{
  "plant_id": "scallions_001",
  "common_name": "Scallions",
  "current_location": {
    "location": "Panel 8",
    "container_name": "Garlic & Scallion Box",
    "stake": null,
    "position": "edges"
  }
}
```

**Display in HTML:**
```
Panel 8 — Garlic & Scallion Box

Siberian Hardneck Garlic
  • Position: Left section
  • Container: Window planter 23.5" × 6" (shared)

Music Hardneck Garlic
  • Position: Center section

Scallions
  • Position: Edges
```

### Example 4: Multiple Observations Same Day

Tomato observed multiple times on 11/11:

```json
{
  "date": "20251111",
  "plant_observations": [
    {
      "plant_id": "tomato_001",
      "time": "0900",
      "observations": "Morning check - plant still covered from overnight",
      "actions_taken": ["Removed cover"],
      "photos": []
    },
    {
      "plant_id": "tomato_001",
      "time": "1500",
      "soil_moisture": "dry 1 inch down",
      "observations": "Afternoon - noticed speckled leaves and first fruits!",
      "actions_taken": [
        "Pruned diseased branches",
        "Watered deeply",
        "Added mulch",
        "Watered mulch"
      ],
      "photos": [
        {
          "filename": "tomato_001_20251111_1445_1.jpg",
          "timestamp": "1445",
          "tags": ["before_pruning"],
          "caption": "Before pruning"
        },
        {
          "filename": "tomato_001_20251111_1530_1.jpg",
          "timestamp": "1530",
          "tags": ["after_pruning", "after_mulching"],
          "caption": "After all work completed"
        }
      ]
    }
  ]
}
```

---

## Conventions

### Dates
Always use `YYYYMMDD` format (e.g., "20251111")

### Times
Always use 24-hour military time `HHMM` (e.g., "1400" for 2:00 PM)

### Plant IDs
Format: `{planttype}_{###}` with 3-digit numbers (e.g., "basil_001")

### Container Names
Use friendly, descriptive names:
- Individual: "Basil Pot - Left", "Tomato Pot"
- Shared: "Pepper Box", "Garlic & Scallion Box", "5-Herb Box"
- Large: "Raised Bed"

### Stakes
Number from 1 upward, restart at 1 for each container

### Positions
Use descriptive text:
- "left section", "right section", "center section"
- "edges", "corners"
- "left side", "right side"

### Temperatures
Always use Fahrenheit (°F)

### Amounts
Use common measurements:
- Cups: "½ cup", "1½ cups", "2 cups"
- Ounces: "8 oz", "16 oz"
- Tablespoons: "2 tbsp", "3 tbsp"
- Layers: "1 inch layer", "thin layer"

---

## Tips

### Recording Multiple Observations

If you check a plant multiple times in one day:
- Create separate observation entries with different times
- Link photos to the correct time observation
- Track actions separately for each check

### Photo Organization

- Use tags to categorize photos
- Add captions for context
- Link before/after photos with consistent tags
- Maximum 4 photos displayed per observation in HTML

### Shared Containers

**With Stakes:**
- Use stake numbers (1, 2, 3, 4)
- Pepper Box, Raised Bed

**Without Stakes:**
- Use position descriptions
- Garlic Box, Herb Box, Arugula/Cilantro Box

### Tracking Temporary Moves

Always record:
- When it moved temporarily
- Why (cold protection, pest treatment, etc.)
- When it returned (if it did)

---

## See Also

- [Photo Naming Convention](photo-naming.md)
- [Daily Workflow](workflow.md)
- [Setup Instructions](setup.md)
- `src/schema.py` - Python validation and data classes