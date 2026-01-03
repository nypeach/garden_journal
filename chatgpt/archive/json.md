```json
{
  "date": "M/D/YYYY",
  "time": "H:MM AM/PM",
  "conditions": "Weather narrative including High/Low/Condition",
  "digital_probe": {
    "ph": "#0.00",
    "ec_mScm": "#0.00",
    "salt_mg_L": "##0",
    "moisture_mScm": "#0",
    "light": "#0",
    "rh_percent": "#0%",
    "fertility_percent": "#0.0",
    "soil_temp_f": "#0.0"
  },
  "analog_probe": {
    "fertility": "Text description or empty",
    "moisture": "Text description or empty",
    "ph": "Text description or empty"
  },
  "observations": "What the plant looks like RIGHT NOW",
  "actions": "What to do RIGHT NOW (present tense)",
  "next_steps": "Monitoring and future care",
  "q_and_a_summary": "Summary Narrative of real questions asked and answers given",
  "follow_up": [
    "[H:MM AM/PM] Narrative summary of action/observation"
  ],
  "photos": [
    {
      "file_name": "{plantname_001}-{YYYYMMDD}-{nn}.jpeg",
      "caption": "Complete sentence description",
      "tags": "comma, separated, keywords"
    }
  ]
}
```

```json
{
  "common_name": "common name of the plant",
  "type": "type of inventory item",
  "manufacturer": "name of the manufacturer",
  "manufacturer_instructions": "manfuacturer instructions",
  "ready_to_use": boolean,
  "dilution_instructions": "mixing instructions or empty string if ready_to_use",
  "per_container_usage": [
    {
      "common_name": "parent common_name",
      "amount_per_item": "amount to use per item"
    },
    {
      "common_name": "parent common_name",
      "amount_per_item": "amount to use per item"
    }
  ],
  "notes": "Balanced NPK for general feeding"
}
```

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
    "container_dimensions": {
      "volume": "",
      "dimensions": "",
      "material": ""
    },
    "suitable_for_plants": [
    "",
    "",
    ],
    "notes": ""
  }
]
```