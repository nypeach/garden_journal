# Photo Naming Convention

## Overview

All garden photos use a consistent naming format that embeds metadata directly in the filename.

---

## Format

```
{plant_id}_{YYYYMMDD}_{HHMM}_{seq}.jpg
```

### Components

1. **plant_id** - The plant's unique identifier (matches `plant_id` in JSON)
2. **YYYYMMDD** - Full date (year, month, day)
3. **HHMM** - Time in 24-hour military format
4. **seq** - Photo sequence number (1, 2, 3, 4, ...)

---

## Examples

```
basil_001_20251105_0745_1.jpg
tomato_001_20251105_1430_1.jpg
strawberry_001_20251107_0830_2.jpg
```

---

## Storage Structure

All photos in one flat directory:

```
photos/
├── basil_001_20251029_0745_1.jpg
├── basil_001_20251029_0745_2.jpg
├── tomato_001_20251029_0745_1.jpg
└── ...
```

---

## Military Time Reference

| 12-Hour | 24-Hour |
|---------|---------|
| 7:45 AM | 0745 |
| 12:00 PM | 1200 |
| 2:30 PM | 1430 |
| 5:00 PM | 1700 |

---

## See Also

- [Data Structure](data-structure.md)
- [Workflow Guide](workflow.md)
