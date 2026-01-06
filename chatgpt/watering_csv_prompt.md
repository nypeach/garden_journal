# Plant Watering Matrix Fill-In Prompt (One-Time Exercise)

## Problem We Are Solving
I work crazy hours.  The only consistent time I can get outside is 6:00 AM.  I live in Loxahatchee, FL which can get very hot weather during the day.  I need to be able to go out at 6:00 AM and estimate based on certain conditions if I should water and how much.  Sometimes I don't get out until close to 3:00 PM and the plant could be sitting in 80+ degree full sun all day.  So I am creating a chart for myself that based on these conditions so I can easily estimate what to do at 6:00 AM regarding watering.

## Your Role
As my expert **professional horticulturist or extension agent** your job is to take the inputs I provide plus the channel chat history and Fill in the CSV template below for **THIS specific plant** so that the **exact text in each cell** is the *final* watering instruction I should follow at **6:00 AM**.

## Goal
Fill in the CSV template below for: **{plant_id}**

### Important Rules
1. **Each cell must contain a final instruction** (not a percent, not a formula).
   - Examples:
     - `Don't water`
     - `Water 1/4 cup`
     - `Water 1/2 cup slowly around base`
     - `Water 1/2 cup in a circle 1/2" from the crown`
2. **Use consistent wording across the sheet** (same phrasing style for similar actions).
3. **Assume I am using an analog moisture probe at 6:00 AM**:
   - `Dry (0-3)`
   - `Normal (3-7)`
   - `Wet (7-10)`
4. **Temperature columns are the expected HIGH for the day**.
5. **Precip Range** reflects today’s forecasted chance of precipitation.
6. **Bring Inside/Cover** is a single constant threshold for the plant (same for every row).
   - Replace "< ??°F" with actual temperature amount for this plant.  Fill it as: `< XX°F` (example: `< 50°F`)
7. If you are unsure between two watering amounts, choose the more **conservative** option that avoids overwatering, *unless* the plant is known to wilt fast (then bias slightly toward watering).
8. Take into consideration the number of hours the plant is in the sun and that this is Florida with high temperatures.

### Output Expectations
- Return the completed CSV template (same structure) with every empty cell filled in.
- Keep units simple (only these measurable increments) plus the Method:
  1/8 cup, 1/4 cup, 1/2 cup, 3/4 cup, 1 cup, 1.5 cups, 1 pint, 1 quart, 1.5 quarts, 1 gallon, 1.5 gallons, 2 gallons
- If you recommend “don’t water,” use exactly: `Don't water`

### Inputs
`{put inputs here}`

---
## CSV TEMPLATE (ALL 36 ROWS FOR ONE PLANT)
```csv
id,Bring Inside/Cover,Precip Range,Condition,6AM Moisture,60-65°F,66-70°F,71-75°F,76-80°F,81-85°F,86-90°F,90+°F
{plant_id},< ??°F,0-25%,Sunny,Dry (0-3),,,,,,,
{plant_id},< ??°F,0-25%,Sunny,Normal (3-7),,,,,,,
{plant_id},< ??°F,0-25%,Sunny,Wet (7-10),,,,,,,
{plant_id},< ??°F,0-25%,Partly Cloudy,Dry (0-3),,,,,,,
{plant_id},< ??°F,0-25%,Partly Cloudy,Normal (3-7),,,,,,,
{plant_id},< ??°F,0-25%,Partly Cloudy,Wet (7-10),,,,,,,
{plant_id},< ??°F,0-25%,Cloudy,Dry (0-3),,,,,,,
{plant_id},< ??°F,0-25%,Cloudy,Normal (3-7),,,,,,,
{plant_id},< ??°F,0-25%,Cloudy,Wet (7-10),,,,,,,
{plant_id},< ??°F,26-50%,Sunny,Dry (0-3),,,,,,,
{plant_id},< ??°F,26-50%,Sunny,Normal (3-7),,,,,,,
{plant_id},< ??°F,26-50%,Sunny,Wet (7-10),,,,,,,
{plant_id},< ??°F,26-50%,Partly Cloudy,Dry (0-3),,,,,,,
{plant_id},< ??°F,26-50%,Partly Cloudy,Normal (3-7),,,,,,,
{plant_id},< ??°F,26-50%,Partly Cloudy,Wet (7-10),,,,,,,
{plant_id},< ??°F,26-50%,Cloudy,Dry (0-3),,,,,,,
{plant_id},< ??°F,26-50%,Cloudy,Normal (3-7),,,,,,,
{plant_id},< ??°F,26-50%,Cloudy,Wet (7-10),,,,,,,
{plant_id},< ??°F,51-75%,Sunny,Dry (0-3),,,,,,,
{plant_id},< ??°F,51-75%,Sunny,Normal (3-7),,,,,,,
{plant_id},< ??°F,51-75%,Sunny,Wet (7-10),,,,,,,
{plant_id},< ??°F,51-75%,Partly Cloudy,Dry (0-3),,,,,,,
{plant_id},< ??°F,51-75%,Partly Cloudy,Normal (3-7),,,,,,,
{plant_id},< ??°F,51-75%,Partly Cloudy,Wet (7-10),,,,,,,
{plant_id},< ??°F,51-75%,Cloudy,Dry (0-3),,,,,,,
{plant_id},< ??°F,51-75%,Cloudy,Normal (3-7),,,,,,,
{plant_id},< ??°F,51-75%,Cloudy,Wet (7-10),,,,,,,
{plant_id},< ??°F,76-100%,Sunny,Dry (0-3),,,,,,,
{plant_id},< ??°F,76-100%,Sunny,Normal (3-7),,,,,,,
{plant_id},< ??°F,76-100%,Sunny,Wet (7-10),,,,,,,
{plant_id},< ??°F,76-100%,Partly Cloudy,Dry (0-3),,,,,,,
{plant_id},< ??°F,76-100%,Partly Cloudy,Normal (3-7),,,,,,,
{plant_id},< ??°F,76-100%,Partly Cloudy,Wet (7-10),,,,,,,
{plant_id},< ??°F,76-100%,Cloudy,Dry (0-3),,,,,,,
{plant_id},< ??°F,76-100%,Cloudy,Normal (3-7),,,,,,,
{plant_id},< ??°F,76-100%,Cloudy,Wet (7-10),,,,,,,
```

---
## Your Immediate Instructions

Provide a quick bulleted list only of your understanding of what I am asking you to do following by a sample code block of the first 9 rows for this actual plant.
