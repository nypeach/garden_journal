===============================================
# 🌿 Master Garden Inventory Schema
_Last Updated: January 3, 2026 8:15 AM EST_
===============================================

## Overview

This inventory serves as the single source of truth for all garden products and containers. AI Assistant uses this inventory to:

- Recommend products already on hand (inventory-first guidance)
- Calculate precise application rates based on the specific container dimensions each plant is in
- Reference container specifications when advising on transplanting
- Provide manufacturer-based guidance tailored to actual container sizes

Plants reference containers by `common_name`, and AI Assistant looks up container dimensions and product usage rates from this unified inventory to ensure all recommendations are specific, accurate, and based on what is actually in inventory.

## Inventory JSON Structure
```json
[
  {
    "common_name": "",
    "type": "",
    "manufacturer": "",
    "manufacturer_instructions": "",
    "ready_to_use": true,
    "dilution_instructions": "",
    "conversions": [
      {
        "water_volume": "",
        "product_amount": ""
      }
    ],
    "container_specifications": {
      "volume": "",
      "dimensions": "",
      "material": ""
    },
    "suitable_for_plants": [],
    "notes": ""
  }
]
```

## Field Definitions

Below are the field definitions for the **Inventory** JSON:

- `common_name` (string, required, unique): The name used to reference this product or container
- `type` (string, required): Category of the product. One of:
  - `container`: Pots, planters, grow bags, etc.
  - `plant_nutrition`: Fertilizers, nutrients, growth regulators
  - `pest_control`: Pesticides, fungicides, insecticides
  - `ph_balance`: pH adjusters (lime, sulfur, etc.)
  - `soil_amendment`: Compost, amendments, soil conditioners
  - `tools_accessories`: Support structures, ties, tools, covers, etc.

- `manufacturer` (string, optional): Brand or manufacturer name
- `manufacturer_instructions` (string, optional): Key details from manufacturer instructions relevant to gardening purposes
- `ready_to_use` (boolean, optional): `true` if product is ready to apply directly, `false` if requires dilution or mixing. Omit for containers and tools/accessories
- `dilution_instructions` (string, optional): How to dilute the product if `ready_to_use` is `false`. Only present when `ready_to_use` is `false`
- `conversions` (array of objects, optional): Dilution conversion table - ONLY for products where `ready_to_use` is `false`
  - `water_volume` (string, required): Amount of water (e.g., "1/4 cup", "1 pint", "1 gallon")
  - `concentrate` (string, required): Amount of concentrate to add to that water volume (e.g., "1/12 tsp (~0.42 mL)", "2 tsp (~10 mL)")

- `container_specifications` (object, optional): Physical specifications - ONLY for products where `type` is `container`
  - `volume` (string, optional): Container volume capacity (e.g., "5 gallon", "2 quart")
  - `dimensions` (string, optional): Physical measurements including top/bottom width, length, depth, height (e.g., "23.5 inch W top, 20.3 inch W bottom × 7.8 inch L × 6 inch D")
  - `material` (string, optional): Container material (e.g., "fabric", "plastic", "ceramic")

- `suitable_for_plants` (array of strings, optional): ONLY for containers - list of mature plant types that can fit in this container size (e.g., ["basil", "cilantro", "parsley", "dill"] or ["tomatoes (determinate)", "peppers", "eggplant", "cucumbers (with trellis)"])
- `notes` (string, optional): Additional context, warnings, or usage notes