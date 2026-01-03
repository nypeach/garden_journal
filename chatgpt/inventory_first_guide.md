===============================================
# 🌿 Master Garden Inventory First Guide
_Last Updated: January 3, 2026 5:31 AM_
===============================================

The assistant will provide "Hose First Watering" instructions as outlined in the `docs/expert_assessment_guide.md`.  The instructions regarding watering in THIS guide are for when a product in inventory needs to be used specifically with watering (either diluted, watered in etc.)


## Inventory First Rule

- **Prefer inventory products first** for all recommendations.
- If no inventory product fits the situation, **recommend a substitute** and still provide **exact measurements** where applicable
- For any recommendation involving mixing or dosing, always give:
   - **Water volume**
   - **Exact product amount**
   - **Application instructions**
   - No vague language (“a little”, “some”, “half strength”, etc.)
- All guidance must be tailored to the **exact container dimensions which include size, volume, material, drainage, and soil** as defined in:

### Container-Specific Instructions

 The following instructions are only applicable when - The `container` attribute is located in the `{plant_id}.json` file located in the `data/plants` folder in the repo
- The `container` attribute exactly matches the unique `common_name` attribute in the `data/inventory.json`
- All guidance must be tailored to the **exact container `volume` and `dimensions` in the `inventory.json` file

The assistant must **NEVER**
- Ask the user for container size or type
- Guess or invent quantities
- Reference manufacturer’s rate, label, instructions
- Estimate container volume from photos or “typical pot sizes”

The assistant must **ALWAYS**
- Get the `container` from the `{plant_id}.json` and look up the matching the `common_name` in the `inventory.json` before giving any scaled quantities
- Scale watering, fertilizer, amendments, and spray volumes to the container’s real capacity
  - *Example: Do NOT recommend mixing 2 gallons for a 16-oz pot*

___


## Plant Nutrition (Liquid Concentrates)
- Use **fertility + moisture** readings and the plant’s **container** to select the correct **watering amount**- Use the product’s `conversions` table to select the exact `product_amount` for that `water_volume`.
- Output must include: **Mix X `water_volume` + `product_amount` of product + **Method**

**🚫 Bad Examples**
"Go light (¼-strength) so we don’t swing the EC upward abruptly."
"Feed lightly using Purived 4-5-5 (1 capful per gallon), then apply 3 cups of the mixed solution."

**✅ Good Examples**
"Mix ⅛ tsp with 2 cups of water, then apply slowly at the base until the top 1–2 inches of soil is evenly moistened."
"Mix ⅜ teaspoon of Purived 4-5-5 into 3 cups of water, then apply the full 3 cups slowly at the base."

___

## pH Balance
- Use **fertility + moisture** readings and the plant’s **container** to select the correct **watering amount**

- If there **IS** a product’s `conversions` table
   - Use the product’s `conversions` table to select the exact `product_amount` for that `water_volume`.

- If there’s **NO** conversion table, assistants must use:
   - Use the plant’s pH trend + container size to select the right **water volume** and **product amount**
   - Output must include:
      - Water Additive: Mix X **water volume** + Y **product amount** + **Method**
      - Non-Water Additive: Apply Y **product amount** + **Method** (top dress + scratch in) + **Water In/Don't Water In**
___

## Pest Control
- Output must include: **Product + Method**

**✅ Good Examples**
"Spray Bonide Captain Jack's DeadBug at dusk. Avoiding direct spraying of open flowers."

___

## Soil Amendments (Non-pH)
- Use **moisture + fertility** readings and container size to determine the correct amendment amount.
- Output must include: **Exact amount + Method + Timing.**

___

## Tools & Accessories
- Output must include: **Tool + Exact steps (1–3 steps).**

___

## Containers (If Transplant is Recommended)
- Output must include: **Exact container recommendation + Repot steps (1–4 steps).**