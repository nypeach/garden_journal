===============================================
# 🌿 Master Garden Inventory First Guide
_Last Updated: January 3, 2026 5:31 AM_
===============================================

## Inventory First Rule
1. **Prefer inventory products first** for all recommendations.
2. If no inventory product fits the situation, **recommend a substitute** and still provide **exact measurements** (mix + apply) using the container’s watering amount.
3. For any recommendation involving mixing or dosing, always give:
   - **Water volume**
   - **Exact product amount**
   - **Application instructions**
   - No vague language (“a little”, “some”, “half strength”, etc.)

___

## Plant Nutrition (Liquid Concentrates)
- Use **fertility + moisture** readings and the plant’s **container** to select the correct **watering amount**
- Use the product’s `conversions` table to select the exact `product_amount` for that `water_volume`.
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