Create a compact watering ruleset for plant_id basil_001 using ONLY these bucket labels (exact strings):

probe_time: 6-8 am, 8-10, 10-12, 12-2, 2-4, 4-6, 7+
current_time: 6-8 am, 8-10, 10-12, 12-2, 2-4, 4-6, 7+
today_high: 65-70, 70-75, 75-80, 80-85, 85-90, 90-95, 95+
today_low: 70-75, 65-70, 60-65, 55-60, 50-55, <50
probe_moisture: 0, 1-25%, 25-35%, 35-50%, 50-65%, >65%
today_precip_chance: 0–20%, 20–40%, 40–60%, 60–80%, 80–100%
tomorrow_precip_chance: 0–20%, 20–40%, 40–60%, 60–80%, 80–100%

Plant context (use as constants):
- location: Loxahatchee, FL
- container: round pot, 0.94 gal
- soil_mix: Nursery Potting Mix
- full_sun_start: 8am
- shade_start: 3pm

Output ONLY valid JSON with this structure:
```json
{
  "plant_id": "basil_001",
  "full_sun_start": "8:00 AM",
  "shade_start": "3:00 PM",
  "watering_profile": {
    "container_gal": 0.94,
    "soil_mix": "Nursery Potting Mix",
    "notes": "short sentence"
  },
  "rules": [
    {
      "priority": 100,
      "conditions": { ... },
      "recommendation": "Skip Watering | Light Sip | Moderate Shower | Deep Water",
      "reasoning": "short, plant-specific"
    }
  ]
}
```

Constraints:
- Create 20–35 rules max, plus 1 default fallback rule.
- Use “Check Probe” recommendation whenever probe_moisture = 0 (include reasoning).
- Put rules in strict priority order (higher wins).
- Do NOT output the full combination grid. Do NOT include any extra keys beyond the schema above.



===============
PROMPT

You are generating a ONE-TIME static JSON ruleset for my watering dashboard.

CRITICAL:
- Output ONLY valid JSON (no commentary, no markdown, no code fences).
- Follow the exact schema/keys below. Do not add, remove, or rename fields.
- Use ONLY the allowed bucket values I provide.
- Create a rule row for EVERY combination of buckets (full cartesian product) for this plant.
- Recommendations must be horticulturist-expert decisions (one clear recommendation per combo, not options).

PLANT CONTEXT (use this to tune recommendations):
- plant_id: {plant_id}
- plant: {plant_name}
- container: {container_description_and_volume}
- soil_mix: {soil_mix}
- full_sun_start: {HH:MM AM}
- shade_start: {HH:MM PM}
- rainfall_exposure: {open_to_rain | partially_sheltered | covered}

BUCKETS (you must only use these exact strings):
- probe_time: ["6-8 AM","8-10 AM","10-12 PM","12-2 PM","2-4 PM","4-6 PM","7+ PM"]
- current_time: ["6-8 AM","8-10 AM","10-12 PM","12-2 PM","2-4 PM","4-6 PM","7+ PM"]
- today_high: ["65-70°F","70-75°F","75-80°F","80-85°F","85-90°F","90-95°F","95+°F"]
- today_low: ["<50°F","50-55°F","55-60°F","60-65°F","65-70°F","70-75°F"]
- probe_moisture: ["0","1-25%","25-35%","35-50%","50-65%",">65%"]
- today_precip_chance: ["0-25%","25-50%","50-75%","75-100%"]
- tomorrow_precip_chance: ["0-25%","25-50%","50-75%","75-100%"]

OUTPUT JSON SCHEMA (exact):
```json
{
  "watering_rules": [
    {
      "plant_id": "string",
      "plant": "string",
      "container": "string",
      "soil_mix": "string",
      "full_sun_start": "HH:MM AM",
      "shade_start": "HH:MM PM",
      "rainfall_exposure": "open_to_rain | partially_sheltered | covered",
      "rules": [
        {
          "conditions": {
            "probe_time": "bucket string",
            "current_time": "bucket string",
            "today_high": "bucket string",
            "today_low": "bucket string",
            "probe_moisture": "bucket string",
            "today_precip_chance": "bucket string",
            "tomorrow_precip_chance": "bucket string"
          },
          "recommendation": "one of: Skip Watering | Light Top-Up | Moderate Watering | Deep Watering",
          "amount": "plain language amount for THIS plant/container (e.g., '1/2 cup', '1 cup', '2 cups', 'slow soak until first drainage')",
          "timing": "Now | Wait until <time window> | Re-check in <time window>",
          "reasoning": "1-2 short sentences tying moisture + heat + precip + time lag + sun window to the recommendation"
        }
      ]
    }
  ]
}
```

RECOMMENDATION DEFINITIONS (HOSE-FIRST, MUST FOLLOW):

All watering recommendations must assume hose watering FIRST.
Only use container-style phrasing if hose watering does not make sense for this plant/location.

Use ONLY the following recommendation labels and meanings:

- **Skip Watering**
  → Do not water now.

- **Light Shower**
  → Hose spray just enough to moisten the top layer of soil.
  → No runoff expected.
  → Used to refresh surface moisture or reduce heat stress.

- **Moderate Watering**
  → Hose watering for **X seconds** at a steady rate.
  → Goal: moisten the active root zone without prolonged runoff.
  → Typically one continuous pass.

- **Deep Watering**
  → Hose watering **slow and steady for X seconds or minutes**.
  → Pause **X minutes**, then repeat once.
  → Goal: fully recharge the container/root zone with visible first drainage.

TIMING FIELD:
- "Now" → water immediately at current_time.
- "Wait until <time window>" → specify a clear window (e.g., "after 6 PM", "tomorrow morning").
- "Re-check in <time window>" → specify when another probe/visual check should occur.

AMOUNT FIELD:
- Must be expressed in **hose time** (seconds or minutes), not volume.
- Example formats:
  - "15–20 seconds"
  - "30 seconds, steady spray"
  - "2 minutes, slow soak; wait 10 minutes; repeat 2 minutes"



=================
CLAUDE NOTES


I think this is right.  We need to create a schema and a prompt that makes sense.  I think we should have more pills per each and narrower ranges



probe time: 6-8 am, 8-10, 10-12, 12-2, 2-4, 4-6, 7+

current time: same as probe time

high temp: 65-70, 70-75, 75-80,80-85 ... through 95 and then 95+ at 5 degree increments

low temp: 70-75, 70-65, 65-60 ... etc through 50 then < 50

probe_moisture: 0, 1-25%, 25-35%, 35-50%, 50-65%, >65%

today_precip_chance: 0–20%, 20–40%, 40–60%, 60–100%

tomorrow_precip_chance: 0–20%, 20–40%, 40–60%, 60–100%


=====================================================
Panel by Panel Sun
Panel 1: full sun start ~9:05 AM, full sun end ~3:31 PM
Panel 2: full sun start ~9:05 AM, full sun end ~3:31 PM
Panel 3: full sun start ~9:00 AM, full sun end ~3:36 PM
Panel 4: full sun start ~9:00 AM, full sun end ~3:36 PM
Panel 5: full sun start ~8:30 AM, full sun end ~4:06 PM
Panel 6: full sun start ~8:30 AM, full sun end ~4:06 PM
Panel 7: full sun start ~9:10 AM, full sun end ~3:26 PM
Panel 8: full sun start ~9:45 AM, full sun end ~2:51 PM
Panel 9: full sun start ~10:20 AM, full sun end ~2:16 PM
Panel 10: full sun start ~10:43 AM, full sun end ~1:53 PM
Panel 11: full sun start ~10:43 AM, full sun end ~1:53 PM
Panel 12: full sun start ~10:43 AM, full sun end ~1:53 PM
Panel 13: full sun start ~10:43 AM, full sun end ~1:53 PM
Panel 14: full sun start ~10:48 AM, full sun end ~1:48 PM
Panel 15: full sun start ~10:48 AM, full sun end ~1:48 PM
Panel 16: full sun start ~11:00 AM (estimated), full sun end ~1:36 PM (estimated)
Panel 17: full sun start ~11:00 AM (estimated), full sun end ~1:36 PM (estimated)
Panel 18: full sun start ~11:00 AM (estimated), full sun end ~1:36 PM (estimated)

And the two mums by the firepit:
Firepit mum #1: full sun start ~9:30 AM, full sun end ~3:06 PM
Firepit mum #2: full sun start ~9:30 AM, full sun end ~3:06 PM