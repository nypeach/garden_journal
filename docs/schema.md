# 🌿 Master Garden Data Structure
_Last Updated: December 8, 2025 6:39 PM_
===============================================
# Garden Journal Data Structure

**VERSION:** 1
**Last Updated: 2025-12-10**

---

## Overview

The 🌿 Master Garden Dashboard uses multiple JSON files to store all garden data.

## File Location

```
data/meta.json
data/plants.json
data/containers.json
data/products.json

```

## Root Structure

```json
{
  "_schema_version": "1",
  "_last_updated": "2025-12-10",
  "metadata": { },
  "products": [ ],
  "containers": [ ],
  "plants": [ ]
}
```

---

## What's New in Version 1

### New in This Version


---


## Metadata

Basic information about your garden.

```json
{
  "metadata": {
    "garden_name": "Jodi's Garden Journal",
    "start_date": "October 8, 2025",
    "location": "Loxahatchee, Florida",
    "garden_type": "Campsite Fenced Front Yard Garden"
  }
}
```

### Fields

- `garden_name` (string) - Display name for your garden
- `start_date` (string) - Date garden started (MMMM, D, YYYY)
- `location` (string) - Geographic location
- `garden_type` (string) - Type of garden setup

---

## Products Array

Each product in your garden with common_name to use in your journal.

```json
{
  "product_name": "Miracle-Gro Organic Mulch",
  "common_name": "Miracle-Gro Mulch"
}
```

### Required Fields

- `product_name` (string) - Unique identifier
- `common_name` (string) - Display name


## Containers Array

Each container in your garden with common_name to use in your journal.

```json
{
  "container_name": "Raised bed 2' × 6' × 10\", brown, Stake 1",
  "common_name": "Raised Bed (Stake 1)"
}
```

### Required Fields

- `container_name` (string) - Unique identifier
- `common_name` (string) - Display name


## Plants Array

Each plant in your garden with complete history.

```json
{
  "_schema_version": "14",
  "_last_updated": "2025-11-20",
  "metadata": {
    "garden_name": "Jodi's Garden Journal",
    "start_date": "20251008",
    "location": "Miami, Florida",
    "garden_type": "Campsite Fenced Front Yard Garden"
  },
  "products": [
    {
      "product_name": "Miracle-Gro Organic Mulch",
      "common_name": "Miracle-Gro Mulch"
    },
    {
      "product_name": "Miracle-Gro Moisture Control Potting Mix",
      "common_name": "Miracle-Gro Potting Mix"
    },
    {
      "product_name": "Miracle-Gro Organic Potting Mix",
      "common_name": "Miracle-Gro Organic Potting Mix"
    },
    {
      "product_name": "Bonide Captain Jack's Neem Oil",
      "common_name": "Neem Oil"
    },
    {
      "product_name": "BioAdvanced Insect Killer For Soil & Turf",
      "common_name": "Grub & Insect Killer"
    },
    {
      "product_name": "JQ001 3-in-1 Soil Test Kit",
      "common_name": "JQ001"
    },
    {
      "product_name": "8 in 1 pH Moisture Meter Smart Soil Test Kit",
      "common_name": "YINMIK"
    }
  ],
  "containers": [
    {
      "container_name": "Window planter 23.5\" × 6\", black (Stake 1)",
      "common_name": "Pepper Window Box (Stake 1)"
    },
    {
      "container_name": "Window planter 23.5\" × 6\", black (Stake 2)",
      "common_name": "Pepper Window Box (Stake 2)"
    },
    {
      "container_name": "Window planter 23.5\" × 6\", black (Stake 3)",
      "common_name": "Pepper Window Box (Stake 3)"
    },
    {
      "container_name": "Window planter 23.5\" × 6\", black (Garlic Box)",
      "common_name": "Garlic Window Box"
    },
    {
      "container_name": "Window planter 23.5\" × 6\", black (5 Herb Box)",
      "common_name": "5 Herb Window Box"
    },
    {
      "container_name": "Window planter 23.5\" × 6\", black",
      "common_name": "Window Box"
    },
    {
      "container_name": "Raised bed 2' × 6' × 10\", brown (Stake 1)",
      "common_name": "Raised Bed (Stake 1)"
    },
    {
      "container_name": "Raised bed 2' × 6' × 10\", brown (Stake 2)",
      "common_name": "Raised Bed (Stake 2)"
    },
    {
      "container_name": "Raised bed 2' × 6' × 10\", brown (Stake 3)",
      "common_name": "Raised Bed (Stake 3)"
    },
    {
      "container_name": "Raised bed 2' × 6' × 10\", brown (Stake 4)",
      "common_name": "Raised Bed (Stake 4)"
    },
    {
      "container_name": "Bonnie Plants Foodie Fresh Pot, 0.94 gal, white",
      "common_name": "Round pot, 0.94 gal, white"
    },
    {
      "container_name": "Bonnie Plants, 2.32 qt pot, black",
      "common_name": "Round pot, 2.32 qt, black"
    },
    {
      "container_name": "Bonnie Plants Foodie Fresh Pot, 25 oz pot, white",
      "common_name": "Round pot, 25 oz, white"
    },
    {
      "container_name": "Style Selections Round 6.0-in W x 6.0-in L Black Plastic Indoor/Outdoor Planter",
      "common_name": "Round pot, 6\" 5 qt, black"
    },
    {
      "container_name": "Style Selections Round 8.0-in W x 8.0-in L Black Plastic Indoor/Outdoor Planter",
      "common_name": "Round pot, 8\" 1.5 gal, black"
    }
  ],
  "plants": []
}
```


====== SECTION ======
# 🌿 Plant Data Schema

The **Plant Data** includes:

- The identity, origin, and status of the plant
- A snapshot of the current development stage and state of the plant
- A timeline of what the user can expect to see about the plant at various intervals
- A journal of Daily Journal Entries which include:
   - Time-stamped records of each observation session with environmental conditions
   - Digital and analog probe measurements capturing soil health metrics
   - Detailed observations of plant appearance, growth patterns, and any issues
   - Actions taken and recommendations for future care
   - Documentation of questions, answers, follow-up notes, and tagged photos


Each **Plant Data** profile must follow this structure:

```json
{
  "id": "plantname_001",
  "status": "Active",
  "plant": "Plant Name (Variety)",
  "physical_location": "City, ST",
  "garden_location": "Location Description",
  "container": "Container Type",
  "soil_mix": "Soil Product Name",
  "origin_history": [
    "Event on Date",
    "Event on Date"
  ],
  "whats_been_logged": "Narrative summary paragraph",
  "current_stage": "Growth Stage",
  "current_state": "Visual description paragraph",
  "timeline": [
    {
      "what_i_should_see": "Observable milestone",
      "date_range": "Mmm DD - Mmm DD, YYYY"
    }
  ],
  "journal": [
    {
      "date": "M/D/YYYY",
      "time": "H:MM AM/PM",
      "conditions": "Weather narrative (High/Low/Condition)",
      "digital_probe": {
        "ph": "6.50",
        "ec_mScm": "0.02",
        "salt_mg_L": "139",
        "moisture_mScm": "49.00",
        "light": "99",
        "rh_percent": "45",
        "fertility_percent": "1.0",
        "soil_temp_f": "85.5"
      },
      "analog_probe": {
        "fertility": "Text description or empty",
        "moisture": "Text description or empty",
        "ph": "Text description or empty"
      },
      "observations": "What the plant looks like RIGHT NOW",
      "actions": "What to do RIGHT NOW (present tense)",
      "next_steps": "Monitoring and future care",
      "q_and_a_summary": "Questions asked and answers given",
      "follow_up": [
        "[H:MM AM/PM] Narrative summary of action/observation"
      ],
      "photos": [
        {
          "file_name": "<<put filename here>>",
          "caption": "Complete sentence description",
          "tags": "comma, separated, keywords"
        }
      ]
    }
  ]
}
```

___

## Plant Main Data Field Definitions

Below are the field definitions for the **Plant Main Data**:

- `id` (string, required): Unique identifier for the plant entry. Must follow the pattern `plantname_###` (See "ID Rules" below)
- `status`(string, required): "Active" or "Inactive" only
- `plant` (string, required): Common name of the plant
- `physical_location` (string, required): Geographic location where the plant is grown
- `garden_location` (string, required): Specific location within the garden (e.g., "Fence Panel 11")
- `container` (string, required): Type of container used for the plant
- `soil_mix` (string, required): Description of the soil mixture composition
- `origin_history` (array of strings, required): Chronological list of significant events in the plant's history (See "Origin History Rules" below)
- `whats_been_logged` (string, required): Summary of what has been tracked and recorded
- `current_stage` (string, required): Current growth stage of the plant
- `current_state` (string, required): Detailed description of the plant's current condition
- `timeline` (array of objects, required): Expected visual milestones with projected date ranges (See "Timeline Rules" below)
- `journal` (array of objects, required): Daily log entries following the structure in Section 5.1

___

## Plant Main Data Field Formatting

It is important to note that the field formatting is only for the aesthetics of how the field should be formatted. All rules related to the fields will be found in the **Plant Main Data Update Rules** _(ref 6.8)_ section.

The **Plant Main Data Field Formatting** section includes:

- A. **ID** Field Formatting
- B. **Status** Field Formatting
- C. **Plant** Field Formatting
- D. **Physical Location** Field Formatting
- E. **Garden Location** Field Formatting
- F. **Container** Field Formatting
- G. **Soil Mix** Field Formatting
- H. **Origin History** Formatting
- I. **What's Been Logged** Formatting
- J. **Current Stage** Formatting
- K. **Timeline** Formatting
- L. **String Field** Formatting

___

### A. **ID** Field Formatting

- Format: `{plant_name}_{number}`
- Plant name portion must be lowercase letters or underscores only
- Number portion must be exactly 3 digits
- Examples: "arugula_001", "cherry_tomato_042"
- Each **ID** must be unique across all plant entries

___

### B. **Status** Field Formatting

- Format: "Active" or "Inactive"
- Only one of these two formats

___

### C. **Plant** Field Formatting

- Format: `plant`
- 2-3 words
- No periods
- Title Case
- Descriptions should be in Parenthesis (ex: "Tomato (Husky Cherry Red)", "Zucchini (Center)")
- Each `plant` value must be unique across all plant entries

___

### D. **Physical Location** Field Formatting

- Format: `{city}, {state}`
- `{city}` should not be abbreviated
- `{state}` should be the US two-letter state abbreviation

___

### E. **Garden Location** Field Formatting

- Format: `{Description of location in the garden}`
- Clarifying descriptions should be in Parenthesis
- Examples: "Picnic Table", "Fence Panel 3", "Fence Panels 16-18", "Raised Bed (Stake 1)", "Fence Panel 3 (Stake 3)"

___

### F. **Container** Field Formatting

- Format: `{Common Name of the Container}`
- Clarifying descriptions should be in Parenthesis
- Examples: "Window Planter", "Raised Bed (Stake 2)", "Round pot, 0.94 gal, white", "Herb Box (Front Left)"

___

### G. **Soil Mix** Field Formatting

- Format: `{Common Name of the Product}`
- Examples: "Miracle-Gro Potting Mix", "Top Soil/Sand"

___

### H. **Origin History** Formatting

- Array of string elements
- Minimum 3 elements required
- Example:

```
"origin_history": [
  "Bought on Oct 8, 2025 (2.32 qt container)",
  "Transplanted into raised bed and staked.",
  "Positioned to receive ~6 hours of full sun daily."
],
```

___

### I. **What's Been Logged** Formatting

- Format: `{Paragraph describing what's been logged}`
- Single Paragraph
- 1-4 Sentences

___

### J. **Current Stage** Formatting

- Format: `{Current Plant Stage for this Plant}`

___

### K. **Timeline** Formatting

- Array of object elements
- Each timeline element must contain:

   - `what_i_should_see` (string, required): Description of expected visual milestones
   - `date_range` (string, required): Expected timeframe

- The `date_range` can be formatted in one of two ways:

   - `{Mmm} {DD}, {YYYY}` _This is for a single date_
   - `{Mmm} {DD} - {Mmm} {DD}, {YYYY}` _This is for a range of dates_

- No periods after the `{Mmm}`
- Use natural language format (e.g., "Nov 20 - Nov 27, 2025" or "Dec 20, 2025")

___

### L. **String Field** Formatting

- All text fields should use complete sentences where appropriate
- Empty strings `""` are acceptable for optional content but all required fields must have values
- Use proper capitalization and punctuation

___

## Plant Journal Data Field Definitions

Below are the field definitions for the **Plant Journal Data**:

- `date` (string, required): Date of entry in `M/D/YYYY` format
- `time` (string, required): Time of entry in `H:MM AM/PM` format
- `conditions` (string, required): Weather and environmental conditions
- `digital_probe` (object, required): Digital probe measurements

   - `ph` (string, required): pH level reading
   - `ec_mScm` (string, required): Electrical conductivity in mS/cm
   - `salt_mg_L` (string, required): Salt concentration in mg/L
   - `moisture_mScm` (string, required): Moisture reading in mS/cm
   - `light` (string, required): Light intensity reading
   - `rh_percent` (string, required): Relative humidity percentage
   - `fertility_percent` (string, required): Fertility percentage
   - `soil_temp_f` (string, required): Soil temperature in Fahrenheit

- `analog_probe` (object, required): Analog probe measurements

   - `fertility` (string, required): Fertility reading or description
   - `moisture` (string, required): Moisture reading or description
   - `ph` (string, required): pH reading or description

- `observations` (string, required): Detailed observations about plant appearance, health, and conditions
- `actions` (string, required): Actions taken during this entry (watering, fertilizing, etc.)
- `next_steps` (string, required): Planned next steps or monitoring recommendations
- `q_and_a_summary` (string, required): Summary of any questions asked and answers provided
- `follow_up` (array of strings, required): Follow-up notes with timestamps
- `photos` (array of objects, required): Photos taken during this entry

   - `file_name` (string, required): Name of the photo file
   - `caption` (string, required): Description of what the photo shows
   - `tags` (string, required): Tags for categorizing the photo (minimum 1 tag)

___

## Plant Journal Data Field Formatting

It is important to note that the field formatting is only for the aesthetics of how the field should be formatted. All rules related to the fields will be found in the **Plant Journal Data Update Rules** _(ref 6.9)_ section.

The **Plant Journal Data Field Formatting** section includes:

- A. **Date and Time** Formatting
- B. **Conditions** Formatting
- C. **Digital Probe** Formatting
- D. **Analog Probe** Formatting
- E. **Observations** Formatting
- F. **Actions** Formatting
- G. **Next Steps** Formatting
- H. **Q&A Summary** Formatting
- I. **Follow-up** Formatting
- J. **Photos** Formatting

___

### A. **Date and Time** Formatting

**Date Formatting**

- Use `M/D/YYYY` format (e.g., "11/23/2025")
- Month and day should be **only** 2 digits
- Year must be 4 digits

**Time Formatting**

- Use `H:MM AM/PM` format (e.g., "1:49 PM" or "11:05 AM")
- Hour can be 1 or 2 digits
- Minutes must be 2 digits
- Must include AM or PM designation

___

### B. **Conditions** Formatting

- Format: `{Paragraph describing conditions}`
- Single Paragraph
- 1-4 Sentences

___

### C. **Digital Probe** Formatting

**Decimal Precision**

- All readings are stored as strings, even numeric values
- Use consistent decimal precision:

   - `ph`: 2 decimal places (e.g., "6.50")
   - `ec_mScm`: 2 decimal places (e.g., "0.02")
   - `moisture_mScm`: 2 decimal places (e.g., "49.00")
   - `fertility_percent`: 1 decimal place (e.g., "1.0")
   - `soil_temp_f`: 1 decimal place (e.g., "85.5")

- Use whole numbers for: `salt_mg_L`, `light`, `rh_percent`
- Empty strings `""` indicate measurement was not taken

___

### D. **Analog Probe** Formatting

- Values can be descriptive text (e.g., "Green (just into range)", "6 (green, ideal)", "6–7 (green, ideal)")
- Empty strings `""` indicate measurement was not taken
- Include color indicators and qualitative assessments when available

___

### E. **Observations** Formatting

- Format: `{Paragraph describing conditions}`
- Single Paragraph
- 1-4 Sentences

___

### F. **Actions** Formatting

- Format: `{Paragraph describing conditions}`
- Single Paragraph
- 1-4 Sentences

___

### G. **Next Steps** Formatting

- Format: `{Paragraph describing conditions}`
- Single Paragraph
- 1-4 Sentences

___

### H. **Q&A Summary** Formatting

- Format: `{Paragraph summarizing questions and answers}`
- Single Paragraph
- 1-4 Sentences
- Use empty string `""` if no Q&A occurred

___

### I. **Follow-up** Formatting

- Format: "[`{H:MM AM/PM}`] `{Paragraph summarizing the follow-up}`"
- Array of string elements
- Each entry should be a timestamped note in brackets
- Example: `"[1:54 PM] Gave it a light shower"`
- List entries in chronological order
- Use empty array `[]` if no follow-ups

___

### J. **Photos** Formatting

- Array of object elements
- Each photo element must contain:

   - `file_name`: "<<put filename here>>"
   - `caption`: Complete sentence describing what the photo shows
   - `tags`: String of lowercase, comma-separated, keywords

- Minimum 1 tag required