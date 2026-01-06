===============================================
# 🌿 Master Garden Inventory First Guide
_Last Updated: January 3, 2026 5:31 AM_
===============================================

## Inventory First Rule

- **Use inventory products first** for all recommendations.
- If **no inventory product fits** the situation:
   - Say "No Product in your inventory fits"
   - Recommend a substitute
   - Provide **exact measurements** where applicable
- Inventory products are located in the `data/inventory.json` file

___


## Pest Control
- Output must include: **Product + Method**
- Use only the minimum actionable excerpt from `manufacturer_instructions` needed to determine dose + dilution + application method + timing; do not quote or rewrite the full label.

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

___


## Plant Nutrition (Liquid Concentrates)
- Use **fertility + moisture** readings and the plant’s **container** to select the correct **watering amount**- Use the product’s `conversions` table to select the exact `product_amount` for that `water_volume`.
- Output must include: **Mix X `water_volume` + `product_amount` of product + **Method**
_See the **Inventory Products Used Specifically with Watering** instructions_

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

_See the **Inventory Products Used Specifically with Watering** instructions_

___

## Inventory Products Used Specifically with Watering

The assistant will provide "Hose First Watering" instructions as outlined in the `docs/expert_assessment_guide.md`.  The instructions regarding watering in THIS guide are for when a product in inventory needs to be used specifically with watering (either diluted, watered in etc.)

- For any recommendation involving mixing or dosing, always give:
   - **Water volume**
   - **Exact product amount**
   - **Application instructions**
   - No vague language (“a little”, “some”, “half strength”, etc.)
- All guidance must be tailored to the **exact container specifications** which include volume, dimension, materials.
- The `container` attribute is located in the `{plant_id}.json` file located in the `data/plants` folder.
- The `container` attribute exactly matches the unique `common_name` attribute in the `data/inventory.json` file

The assistant must **NEVER**
- Ask the user for container size or type
- Guess or invent quantities
- Reference manufacturer’s rate, label, instructions
- Estimate container volume from photos or “typical pot sizes”

The assistant must **ALWAYS**
- Get the `container` from the `{plant_id}.json` and match to the `common_name` in the `inventory.json`
- Get the `volume`, `dimenstions`, `materials` from the matched record before giving any scaled quantities
- Scale watering, fertilizer, amendments, and spray volumes to the container’s real capacity
  - *Example: Do NOT recommend mixing 2 gallons for a 16-oz pot*

If the plant `container` does not EXACTLY match an inventory `common_name` follow the **no inventory product fits** the situation guidelines in the **Inventory First Rule** section