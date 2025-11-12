#!/usr/bin/env python3
"""
=================================================================
Garden Journal Template Setup Script
VERSION: 13
Last Updated: 2025-11-11 @ 5:30 PM
=================================================================

This script creates the CSS file and HTML templates for the garden journal.

Changes in Version 13:
- Updated to work with Version 13 schema
- Support for multiple observations per plant per day with time badges
- Photo metadata with captions and before/after tags
- Soil moisture display field
- Detailed actions with nested bullet lists
- Upcoming Actions section added
- Container grouping (shared containers, stakes, positions)
- Time badges showing when observations were made

Usage:
    python3 setup_templates_V13.py
"""

import os
from pathlib import Path


def create_base_css():
    """Create templates/base.css with all shared styles"""
    content = """/* Garden Journal Base Styles - Version 13 */

:root {
  --green: #216e3a;
  --muted: #5f6b6b;
  --rule: #e6e8eb;
  --bg: #fff;
  --text: #111;
}

/* Reset and Base */
html,
body {
  margin: 0;
  padding: 0;
  background: var(--bg);
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, "Apple Color Emoji", "Segoe UI Emoji";
  color: var(--text);
  line-height: 1.5;
}

/* Container */
main {
  max-width: 880px;
  margin: 32px auto 60px;
  padding: 0 20px;
}

/* Typography */
h1 {
  font-size: 28px;
  margin: 0 0 14px 0;
  display: flex;
  gap: 10px;
  align-items: center;
  color: var(--text);
}

h2 {
  font-size: 18px;
  margin: 26px 0 8px;
  color: var(--text);
  display: flex;
  gap: 8px;
  align-items: center;
}

h2.major-section {
  font-size: 24px;
  margin: 36px 0 12px;
}

h3 {
  font-size: 18px;
  margin: 20px 0 10px;
  color: var(--text);
  font-weight: 700;
  display: flex;
  gap: 8px;
  align-items: center;
}

p {
  margin: 8px 0 12px;
  line-height: 1.6;
}

p.note {
  color: var(--muted);
  font-size: 14px;
  margin-top: 0;
  margin-bottom: 26px;
  font-style: italic;
}

p.lead {
  margin: 8px 0 12px;
  line-height: 1.6;
}

p.empty-state {
  color: var(--muted);
  font-style: italic;
  margin: 8px 0 12px;
}

/* Lists */
ul {
  margin: 8px 0 8px 0px;
  line-height: 1.6;
}

li {
  margin: 6px 0;
}

/* Dividers */
.divider {
  border: 0;
  border-top: 1px solid var(--rule);
  margin: 22px 0;
}

hr {
  border: 0;
  border-top: 1px solid var(--rule);
  margin: 22px 0;
}

/* Panel/Plant Sections */
.panel {
  margin-bottom: 28px;
}

.panel-title {
  font-weight: 700;
  font-size: 18px;
  margin-bottom: 6px;
}

.stake {
  margin: 16px 0 16px 20px;
  padding-bottom: 16px;
}

.stake-title {
  font-weight: 700;
  margin: 12px 0 6px;
  font-size: 16px;
}

.subtle {
  color: var(--muted);
  font-size: 14px;
  margin-top: 2px;
}

/* Q&A Styling */
.qa-section-header {
  font-size: 16px;
  font-weight: 700;
  margin: 16px 0 8px;
  display: flex;
  gap: 6px;
  align-items: center;
}

.qa-item {
  margin: 12px 0 12px 20px;
  padding-left: 16px;
  border-left: 3px solid var(--rule);
}

.qa-question {
  font-weight: 600;
  margin-bottom: 4px;
}

.qa-answer {
  color: #374151;
  line-height: 1.6;
}

/* Photos */
.photo-row {
  display: flex;
  gap: 0.15in;
  flex-wrap: wrap;
  margin-top: 14px;
  margin-left: 20px;
}

.photo {
  width: 2.0in;
  height: 1.5in;
  border-radius: 10px;
  object-fit: cover;
  border: 1px solid var(--rule);
}

.photo-caption {
  font-size: 12px;
  color: var(--muted);
  font-style: italic;
  margin-top: 4px;
  text-align: center;
  max-width: 2.0in;
}

.photo-container {
  display: flex;
  flex-direction: column;
  align-items: center;
}

/* Hide empty photo slots */
.photo-slot {
  display: none;
}

/* Time badges for multiple observations */
.time-badge {
  display: inline-block;
  background: #f0fdf4;
  border: 1px solid #bbf7d0;
  color: #166534;
  font-weight: 600;
  padding: 3px 8px;
  border-radius: 12px;
  font-size: 13px;
  margin-left: 8px;
}

/* Soil moisture indicator */
.soil-moisture {
  color: var(--muted);
  font-size: 14px;
  font-style: italic;
  margin-top: 4px;
}

/* Print Styles - REMOVED for use with Print Friendly & PDF plugin */
"""

    with open('templates/base.css', 'w', encoding='utf-8') as f:
        f.write(content)
    print("✓ Created file: templates/base.css (Version 13)")


def create_daily_journal_template():
    """Create templates/daily_journal_template.html - VERSION 13"""
    content = '''<!doctype html>
<html lang="en">
<!-- Template Version 13 -->

<head>
  <meta charset="utf-8">
  <title>Daily Journal — {{ date }}</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="styles.css">
</head>

<body>
  <main>

    <h1><span class='emoji'>🌿</span>Daily Journal</h1>
    <p class="note">Date: {{ formatted_date }} • Panels 1–18 (left → right); Stakes 1–4 within raised bed</p>
    <hr class="divider" />

    <!-- SUMMARY OF ACTIVITIES -->
    <h2><span class='emoji'>📝</span>Summary of Activities</h2>
    {% if activities and activities|length > 0 %}
    <ul>
      {% for activity in activities %}
      <li>{{ activity }}</li>
      {% endfor %}
    </ul>
    {% else %}
    <p class="empty-state">No activities recorded for this date</p>
    {% endif %}

    <!-- WEATHER / SUN CONDITIONS -->
    <h2><span class='emoji'>☀️</span>Weather / Sun Conditions</h2>
    {% if weather %}
    <ul>
      {% if weather.temp_high and weather.temp_low %}
      <li><strong>Temperature:</strong> {{ weather.temp_low }}°F – {{ weather.temp_high }}°F</li>
      {% endif %}
      {% if weather.conditions %}
      <li><strong>Conditions:</strong> {{ weather.conditions }}</li>
      {% endif %}
      {% if weather.sunrise and weather.sunset %}
      <li><strong>Sun:</strong> Sunrise {{ weather.sunrise }}, Sunset {{ weather.sunset }}</li>
      {% endif %}
      {% if weather.humidity %}
      <li><strong>Humidity:</strong> {{ weather.humidity }}%</li>
      {% endif %}
      {% if weather.wind %}
      <li><strong>Wind:</strong> {{ weather.wind }}</li>
      {% endif %}
      {% if weather.notes %}
      <li><strong>Notes:</strong> {{ weather.notes }}</li>
      {% endif %}
    </ul>
    {% else %}
    <p class="empty-state">No weather update recorded for this date</p>
    {% endif %}

    <!-- GENERAL OBSERVATIONS -->
    <h2><span class='emoji'>📝</span>General Observations</h2>
    {% if observations and observations|length > 0 %}
    <ul>
      {% for observation in observations %}
      <li>{{ observation }}</li>
      {% endfor %}
    </ul>
    {% else %}
    <p class="empty-state">No general observations recorded</p>
    {% endif %}

    <!-- QUESTIONS & ANSWERS (GENERAL) -->
    <h2><span class='emoji'>❓</span>Questions &amp; Answers</h2>
    {% if questions_and_answers and questions_and_answers|length > 0 %}
    {% for qa in questions_and_answers %}
    <div class="qa-item">
      <div class="qa-question">Q: {{ qa.question }}</div>
      <div class="qa-answer">A: {{ qa.answer }}</div>
    </div>
    {% endfor %}
    {% else %}
    <p class="empty-state">No questions &amp; answers today</p>
    {% endif %}

    <!-- UPCOMING ACTIONS -->
    <h2><span class='emoji'>📋</span>Upcoming Actions</h2>
    {% if upcoming_actions and upcoming_actions|length > 0 %}
    <ul>
      {% for action in upcoming_actions %}
      <li>
        <strong>{{ action.description }}</strong>
        {% if action.target_timeframe %} ({{ action.target_timeframe }}){% endif %}
        {% if action.plants_affected and action.plants_affected|length > 0 %}
        <span class="subtle"> — Affects: {{ action.plants_affected|join(', ') }}</span>
        {% endif %}
      </li>
      {% endfor %}
    </ul>
    {% else %}
    <p class="empty-state">No upcoming actions planned</p>
    {% endif %}

    <hr class="divider" />

    <!-- PLANT BY PLANT -->
    <h2 class="major-section"><span class='emoji'>🪴</span>Plant by Plant</h2>
    <p class="note">Each entry lists container, care notes, and photos with observations made throughout the day</p>

    {# This template expects plant_observations_grouped dict from generator #}
    {# Format: {"Panel 1 - Basil Pot - Left": [obs1], "Panel 7 - Pepper Box": [obs1, obs2, obs3]} #}

    {% for container_key, obs_list in plant_observations_grouped.items() %}

    {# Check if multiple plants share this container with stakes #}
    {% if obs_list|length > 1 and obs_list[0].stake %}

      {# Staked container header #}
      <h3>{{ container_key }}</h3>

      {% for obs in obs_list %}
      <div class="stake">
        <div class="stake-title">
          Stake {{ obs.stake }} — {{ obs.plant_id|replace('_', ' ')|title }}
          {% if obs.time %}<span class="time-badge">{{ obs.time }}</span>{% endif %}
        </div>
        <ul>
          <li><strong>Soil Mix:</strong> {{ obs.soil_mix }}</li>
          {% if obs.soil_moisture %}
          <li><strong>Soil Moisture:</strong> {{ obs.soil_moisture }}</li>
          {% endif %}
          <li><strong>Current Stage:</strong> {{ obs.current_stage }}</li>
          <li><strong>Next Stage:</strong> {{ obs.next_stage }}</li>
          <li><strong>Observations:</strong> {{ obs.observations }}</li>
          {% if obs.actions_taken and obs.actions_taken|length > 0 %}
          <li><strong>Actions Taken:</strong>
            <ul style="margin-top: 4px;">
              {% for action in obs.actions_taken %}
              <li style="margin-left: 20px;">{{ action }}</li>
              {% endfor %}
            </ul>
          </li>
          {% endif %}
          {% if obs.notes %}
          <li><strong>Notes:</strong> {{ obs.notes }}</li>
          {% endif %}
        </ul>

        {% if obs.plant_qa %}
        <div class="qa-section-header"><span class='emoji'>❓</span>Questions &amp; Answers</div>
        <div class="qa-item">
          <div class="qa-question">Q: {{ obs.plant_qa.question }}</div>
          <div class="qa-answer">A: {{ obs.plant_qa.answer }}</div>
        </div>
        {% endif %}

        {% if obs.photos and obs.photos|length > 0 %}
        <div class="photo-row">
          {% for photo in obs.photos[:4] %}
          <div class="photo-container">
            <img src="../photos/{{ photo.filename }}" alt="{{ obs.plant_id }}" class="photo">
            {% if photo.caption %}
            <div class="photo-caption">{{ photo.caption }}</div>
            {% endif %}
          </div>
          {% endfor %}
        </div>
        {% endif %}
      </div>
      {% endfor %}

      <hr class="divider" />

    {% else %}
      {# Regular panel or shared container without stakes #}

      {% if obs_list|length > 1 %}
      {# Shared container header (no stakes) #}
      <h3>{{ container_key }}</h3>
      {% endif %}

      {% for obs in obs_list %}
      <div class="panel" {% if obs_list|length > 1 %}style="margin-left: 20px;"{% endif %}>
        <div class="panel-title">
          {% if obs_list|length == 1 %}
          {{ container_key }}
          {% else %}
          {{ obs.plant_id|replace('_', ' ')|title }}
          {% endif %}
          {% if obs.time %}<span class="time-badge">{{ obs.time }}</span>{% endif %}
        </div>
        <ul>
          <li><strong>Container:</strong> {{ obs.container_type }}</li>
          {% if obs.position %}
          <li><strong>Position:</strong> {{ obs.position }}</li>
          {% endif %}
          <li><strong>Soil Mix:</strong> {{ obs.soil_mix }}</li>
          {% if obs.soil_moisture %}
          <li><strong>Soil Moisture:</strong> {{ obs.soil_moisture }}</li>
          {% endif %}
          <li><strong>Current Stage:</strong> {{ obs.current_stage }}</li>
          <li><strong>Next Stage:</strong> {{ obs.next_stage }}</li>
          <li><strong>Observations:</strong> {{ obs.observations }}</li>
          {% if obs.actions_taken and obs.actions_taken|length > 0 %}
          <li><strong>Actions Taken:</strong>
            <ul style="margin-top: 4px;">
              {% for action in obs.actions_taken %}
              <li style="margin-left: 20px;">{{ action }}</li>
              {% endfor %}
            </ul>
          </li>
          {% endif %}
          {% if obs.notes %}
          <li><strong>Notes:</strong> {{ obs.notes }}</li>
          {% endif %}
        </ul>

        {% if obs.plant_qa %}
        <div class="qa-section-header"><span class='emoji'>❓</span>Questions &amp; Answers</div>
        <div class="qa-item">
          <div class="qa-question">Q: {{ obs.plant_qa.question }}</div>
          <div class="qa-answer">A: {{ obs.plant_qa.answer }}</div>
        </div>
        {% endif %}

        {% if obs.photos and obs.photos|length > 0 %}
        <div class="photo-row">
          {% for photo in obs.photos[:4] %}
          <div class="photo-container">
            <img src="../photos/{{ photo.filename }}" alt="{{ obs.plant_id }}" class="photo">
            {% if photo.caption %}
            <div class="photo-caption">{{ photo.caption }}</div>
            {% endif %}
          </div>
          {% endfor %}
        </div>
        {% endif %}
      </div>
      {% endfor %}

      <hr class="divider" />
    {% endif %}

    {% endfor %}

  </main>
</body>

</html>'''

    with open('templates/daily_journal_template.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("✓ Created file: templates/daily_journal_template.html (Version 13)")


def create_sample_html():
    """Create sample with Nov 11, 2025 actual data - VERSION 13"""
    content = '''<!doctype html>
<html lang="en">
<!-- Sample Daily Journal - Version 13 - November 11, 2025 Real Data -->

<head>
  <meta charset="utf-8">
  <title>Daily Journal — November 11, 2025 (SAMPLE V13)</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="base.css">
</head>

<body>
  <main>

    <h1><span class='emoji'>🌿</span>Daily Journal</h1>
    <p class="note">Date: Monday, November 11, 2025 • Panels 1–18 (left → right); Stakes 1–4 within raised bed</p>
    <hr class="divider" />

    <!-- SUMMARY OF ACTIVITIES -->
    <h2><span class='emoji'>📝</span>Summary of Activities</h2>
    <ul>
      <li>Brought basil and strawberry plants back outside after cold night indoors</li>
      <li>Watered multiple plants that were dry from overnight</li>
      <li>Pruned tomato plant - removed all diseased lower branches</li>
      <li>Added 1-1.5" layer of Miracle-Gro Organic Choice mulch to tomato</li>
      <li>Applied Captain Jack's Neem Oil to zucchini Stake 3 and 4</li>
      <li>Removed spotted leaves from Strawberry - Right and added fresh topsoil</li>
      <li>First watering for both lavender seed pots (Day 2 since planting)</li>
      <li>Deep watered garlic planter with hose (16 oz)</li>
    </ul>

    <!-- WEATHER / SUN CONDITIONS -->
    <h2><span class='emoji'>☀️</span>Weather / Sun Conditions</h2>
    <ul>
      <li><strong>Temperature:</strong> 40°F – 68°F</li>
      <li><strong>Conditions:</strong> Sunny and clear</li>
      <li><strong>Sun:</strong> Sunrise 0653, Sunset 1745</li>
      <li><strong>Wind:</strong> Light breeze</li>
      <li><strong>Notes:</strong> Cold night (below 40°F), brought several plants indoors for protection</li>
    </ul>

    <!-- GENERAL OBSERVATIONS -->
    <h2><span class='emoji'>📝</span>General Observations</h2>
    <ul>
      <li>All plants survived the cold night well with no visible damage</li>
      <li>Tomato plant has first fruits forming - major milestone!</li>
      <li>Lavender seeds still not germinated (expected, day 2 of 14-21 days)</li>
      <li>Arugula showing excellent recovery after November 5th reseeding</li>
      <li>Some fungal leaf spot issues on Strawberry - Right and tomato lower leaves</li>
      <li>Many plants needed watering after dry overnight period</li>
    </ul>

    <!-- QUESTIONS & ANSWERS (GENERAL) -->
    <h2><span class='emoji'>❓</span>Questions &amp; Answers</h2>
    <div class="qa-item">
      <div class="qa-question">Q: Should I clean leaves with alcohol or water before applying neem oil?</div>
      <div class="qa-answer">A: Use water, not alcohol. Zucchini leaves are tender and alcohol can damage their protective coating and cause burn spots in sunlight. Use room-temperature water, let dry completely, then apply neem oil.</div>
    </div>

    <!-- UPCOMING ACTIONS -->
    <h2><span class='emoji'>📋</span>Upcoming Actions</h2>
    <ul>
      <li><strong>Apply Captain Jack's neem oil to Strawberry - Right</strong> (tomorrow morning) <span class="subtle">— Affects: strawberry_002</span></li>
      <li><strong>Add potting mix layer to broccoli/chives and reseed chives</strong> (in a few days) <span class="subtle">— Affects: broccoli_001, chives_001</span></li>
      <li><strong>Add mulch to Zucchini Stake 3</strong> (in about a week) <span class="subtle">— Affects: zucchini_003</span></li>
    </ul>

    <hr class="divider" />

    <!-- PLANT BY PLANT -->
    <h2 class="major-section"><span class='emoji'>🪴</span>Plant by Plant</h2>
    <p class="note">Each entry lists container, care notes, and photos with observations made throughout the day</p>

    <!-- Panel 1 - Basil Left -->
    <div class="panel">
      <div class="panel-title">Panel 1 — Basil - Left <span class="time-badge">2:00 PM</span></div>
      <ul>
        <li><strong>Container:</strong> 8" white round pot, 0.94 gal</li>
        <li><strong>Soil Mix:</strong> Original nursery potting mix</li>
        <li><strong>Soil Moisture:</strong> very dry</li>
        <li><strong>Current Stage:</strong> Vegetative</li>
        <li><strong>Next Stage:</strong> Ready for harvest</li>
        <li><strong>Observations:</strong> Plant vibrant and upright. Was brought indoors last night due to temps below 40°F. Soil very dry.</li>
        <li><strong>Actions Taken:</strong>
          <ul style="margin-top: 4px;">
            <li style="margin-left: 20px;">Watered 1½ cups slowly and evenly over soil surface</li>
            <li style="margin-left: 20px;">Checked after 10 minutes, added ½ cup more as top 2" still felt dry</li>
            <li style="margin-left: 20px;">Ensured proper drainage</li>
          </ul>
        </li>
        <li><strong>Notes:</strong> Plant expected to perk up within an hour. Avoiding fertilizer today to let it stabilize after cold night.</li>
      </ul>

      <div class="photo-row">
        <div class="photo-container">
          <img src="sample-basil-left-1.jpg" alt="Basil Left" class="photo">
          <div class="photo-caption">After being brought back outside</div>
        </div>
        <div class="photo-container">
          <img src="sample-basil-left-2.jpg" alt="Basil Left" class="photo">
          <div class="photo-caption">Close-up showing dry soil</div>
        </div>
      </div>
    </div>

    <hr class="divider" />

    <!-- Panel 2 - Basil Right -->
    <div class="panel">
      <div class="panel-title">Panel 2 — Basil - Right <span class="time-badge">2:00 PM</span></div>
      <ul>
        <li><strong>Container:</strong> 8" white round pot, 0.94 gal</li>
        <li><strong>Soil Mix:</strong> Original nursery potting mix</li>
        <li><strong>Soil Moisture:</strong> Top 1 inch dry, moist below</li>
        <li><strong>Current Stage:</strong> Vegetative</li>
        <li><strong>Next Stage:</strong> Ready for harvest</li>
        <li><strong>Observations:</strong> Plant healthy and full with excellent color and strong leaf growth. Top soil dry but moist about 1 inch down.</li>
        <li><strong>Actions Taken:</strong>
          <ul style="margin-top: 4px;">
            <li style="margin-left: 20px;">Watered ½ to ¾ cup (120-180 mL) evenly across soil</li>
            <li style="margin-left: 20px;">Ensured no pooling</li>
          </ul>
        </li>
        <li><strong>Notes:</strong> Light watering to re-moisten upper layer only since lower soil still moist.</li>
      </ul>

      <div class="photo-row">
        <div class="photo-container">
          <img src="sample-basil-right-1.jpg" alt="Basil Right" class="photo">
          <div class="photo-caption">Healthy full growth</div>
        </div>
      </div>
    </div>

    <hr class="divider" />

    <!-- Panel 3 - Strawberry Left -->
    <div class="panel">
      <div class="panel-title">Panel 3 — Strawberry - Left <span class="time-badge">2:00 PM</span></div>
      <ul>
        <li><strong>Container:</strong> 6" round black planter</li>
        <li><strong>Soil Mix:</strong> Nursery potting mix from transplant</li>
        <li><strong>Soil Moisture:</strong> nice and moist</li>
        <li><strong>Current Stage:</strong> Flowering</li>
        <li><strong>Next Stage:</strong> Fruit development</li>
        <li><strong>Observations:</strong> Healthy and well-established after recent transplant. Leaves upright, flower color vibrant. Small brownish spots on lower leaf - likely transplant stress or early sun exposure.</li>
        <li><strong>Actions Taken:</strong>
          <ul style="margin-top: 4px;">
            <li style="margin-left: 20px;">No watering - soil already moist from being indoors</li>
            <li style="margin-left: 20px;">Will check at sunset, water ½ cup only if top inch dry</li>
          </ul>
        </li>
        <li><strong>Notes:</strong> Spots appear minor and not spreading - monitoring for changes.</li>
      </ul>

      <div class="photo-row">
        <div class="photo-container">
          <img src="sample-strawberry-left-1.jpg" alt="Strawberry Left" class="photo">
          <div class="photo-caption">Full plant view</div>
        </div>
        <div class="photo-container">
          <img src="sample-strawberry-left-2.jpg" alt="Strawberry Left" class="photo">
          <div class="photo-caption">Flower close-up</div>
        </div>
        <div class="photo-container">
          <img src="sample-strawberry-left-3.jpg" alt="Strawberry Left" class="photo">
          <div class="photo-caption">Spots on lower leaf</div>
        </div>
      </div>
    </div>

    <hr class="divider" />

    <!-- Panel 4 - Strawberry Right -->
    <div class="panel">
      <div class="panel-title">Panel 4 — Strawberry - Right <span class="time-badge">2:00 PM</span></div>
      <ul>
        <li><strong>Container:</strong> 2.32 qt black pot</li>
        <li><strong>Soil Mix:</strong> Original potting soil + topsoil/sand fill</li>
        <li><strong>Soil Moisture:</strong> still moist</li>
        <li><strong>Current Stage:</strong> Flowering with leaf spot issues</li>
        <li><strong>Next Stage:</strong> Recovery and fruit development</li>
        <li><strong>Observations:</strong> Plant upright with healthy inner growth. Several outer leaves show brown-purple spots consistent with fungal leaf spot (Mycosphaerella). New leaves and crown appear strong.</li>
        <li><strong>Actions Taken:</strong>
          <ul style="margin-top: 4px;">
            <li style="margin-left: 20px;">Removed affected leaves with clean scissors</li>
            <li style="margin-left: 20px;">Lightly loosened topsoil surface for airflow</li>
            <li style="margin-left: 20px;">Added thin layer of fresh topsoil</li>
            <li style="margin-left: 20px;">Retained large upper leaf (few edge spots but still photosynthesizing)</li>
          </ul>
        </li>
        <li><strong>Notes:</strong> Captain Jack's neem oil planned for tomorrow morning (11/12) after 24-48 hour healing period.</li>
      </ul>

      <div class="qa-section-header"><span class='emoji'>❓</span>Questions &amp; Answers</div>
      <div class="qa-item">
        <div class="qa-question">Q: Should I also get rid of this big leaf with a few spots?</div>
        <div class="qa-answer">A: Keep it for now. The veins are strong and green, the leaf surface is firm, and spots aren't spreading inward. It's still actively photosynthesizing. Monitor daily and remove only if spots enlarge or new ones appear near center veins.</div>
      </div>

      <div class="photo-row">
        <div class="photo-container">
          <img src="sample-strawberry-right-before-1.jpg" alt="Strawberry Right" class="photo">
          <div class="photo-caption">Before removing diseased leaves</div>
        </div>
        <div class="photo-container">
          <img src="sample-strawberry-right-1.jpg" alt="Strawberry Right" class="photo">
          <div class="photo-caption">Close-up of leaf spot damage</div>
        </div>
        <div class="photo-container">
          <img src="sample-strawberry-right-after-1.jpg" alt="Strawberry Right" class="photo">
          <div class="photo-caption">After cleanup - large leaf retained</div>
        </div>
      </div>
    </div>

    <hr class="divider" />

    <!-- Panel 11 - Arugula & Cilantro Box (Shared Container) -->
    <h3>Panel 11 — Arugula & Cilantro Box</h3>

    <div class="panel" style="margin-left: 20px;">
      <div class="panel-title">Arugula <span class="time-badge">2:35 PM</span></div>
      <ul>
        <li><strong>Container:</strong> Window planter 23.5" × 6" (shared)</li>
        <li><strong>Position:</strong> Left side</li>
        <li><strong>Soil Mix:</strong> Sand/soil base + potting mix top layer (added 11/05)</li>
        <li><strong>Soil Moisture:</strong> Top 1 inch bone dry, slight moisture below</li>
        <li><strong>Current Stage:</strong> Recovery and new growth</li>
        <li><strong>Next Stage:</strong> Continued vegetative growth</li>
        <li><strong>Observations:</strong> Significant new growth since Nov 5 reseeding! Dense patch of healthy seedlings. Some lighter green leaves near center where thinning damage occurred. Overall excellent recovery.</li>
        <li><strong>Actions Taken:</strong>
          <ul style="margin-top: 4px;">
            <li style="margin-left: 20px;">Watered ½ cup evenly across to re-moisten top layer</li>
          </ul>
        </li>
      </ul>

      <div class="photo-row">
        <div class="photo-container">
          <img src="sample-arugula-1.jpg" alt="Arugula" class="photo">
          <div class="photo-caption">New growth recovering well</div>
        </div>
      </div>
    </div>

    <div class="panel" style="margin-left: 20px;">
      <div class="panel-title">Cilantro <span class="time-badge">2:00 PM</span></div>
      <ul>
        <li><strong>Container:</strong> Window planter 23.5" × 6" (shared)</li>
        <li><strong>Position:</strong> Right side</li>
        <li><strong>Soil Mix:</strong> Sand/soil only (no potting mix)</li>
        <li><strong>Soil Moisture:</strong> evenly moist from morning watering</li>
        <li><strong>Current Stage:</strong> Early vegetative</li>
        <li><strong>Next Stage:</strong> Continued growth</li>
        <li><strong>Observations:</strong> Seedlings showing good density and upright growth. Leaves bright green though a few appear slightly pale (typical for leaner soil). No damping-off or stress.</li>
        <li><strong>Actions Taken:</strong>
          <ul style="margin-top: 4px;">
            <li style="margin-left: 20px;">Watered this morning with arugula</li>
            <li style="margin-left: 20px;">Brought indoors last night for cold protection</li>
          </ul>
        </li>
      </ul>

      <div class="photo-row">
        <div class="photo-container">
          <img src="sample-cilantro-1.jpg" alt="Cilantro" class="photo">
          <div class="photo-caption">Dense healthy seedlings</div>
        </div>
      </div>
    </div>

    <hr class="divider" />

    <!-- Raised Bed - Staked Container -->
    <h3>Raised Bed — Panels 16–18</h3>

    <div class="stake">
      <div class="stake-title">Stake 1 — Cherry Tomato <span class="time-badge">3:00 PM</span></div>
      <ul>
        <li><strong>Soil Mix:</strong> Topsoil + sand</li>
        <li><strong>Soil Moisture:</strong> dry 1 inch down before watering</li>
        <li><strong>Current Stage:</strong> Fruiting</li>
        <li><strong>Next Stage:</strong> Fruit development</li>
        <li><strong>Observations:</strong> Plant vigorous with FIRST FRUITS FORMING! Speckled and browning lower leaves show early blight or bacterial leaf spot. Upper foliage healthy and strong.</li>
        <li><strong>Actions Taken:</strong>
          <ul style="margin-top: 4px;">
            <li style="margin-left: 20px;">Pruned all lower speckled branches (no fruit on removed branches)</li>
            <li style="margin-left: 20px;">Deep watered soil/sand mix at base, avoiding leaves</li>
            <li style="margin-left: 20px;">Added 1-1.5" layer of Miracle-Gro Organic Choice mulch around base</li>
            <li style="margin-left: 20px;">Watered mulch to settle it in and hydrate root zone</li>
          </ul>
        </li>
        <li><strong>Notes:</strong> Plant appears leaner after pruning but structurally healthy. New side shoots will emerge in 5-7 days. Covered with plastic tablecloth last night.</li>
      </ul>

      <div class="qa-section-header"><span class='emoji'>❓</span>Questions &amp; Answers</div>
      <div class="qa-item">
        <div class="qa-question">Q: Will it fill out again? I chopped a lot off.</div>
        <div class="qa-answer">A: Yes absolutely! New side shoots (suckers) will emerge in upper leaf joints within 5-7 days. Because you removed lower branches, the plant redirects energy toward top growth and fruit production. Within 2-3 weeks you'll see thicker midsection with more flower clusters.</div>
      </div>

      <div class="photo-row">
        <div class="photo-container">
          <img src="sample-tomato-before-1.jpg" alt="Tomato before" class="photo">
          <div class="photo-caption">Before pruning - speckled leaves</div>
        </div>
        <div class="photo-container">
          <img src="sample-tomato-before-2.jpg" alt="Tomato before" class="photo">
          <div class="photo-caption">Full plant before work</div>
        </div>
        <div class="photo-container">
          <img src="sample-tomato-before-3.jpg" alt="Tomato before" class="photo">
          <div class="photo-caption">First fruits visible!</div>
        </div>
        <div class="photo-container">
          <img src="sample-tomato-before-4.jpg" alt="Tomato before" class="photo">
          <div class="photo-caption">Diseased leaves close-up</div>
        </div>
      </div>
      <div class="photo-row">
        <div class="photo-container">
          <img src="sample-tomato-after-1.jpg" alt="Tomato after" class="photo">
          <div class="photo-caption">After pruning - clean lower stem</div>
        </div>
        <div class="photo-container">
          <img src="sample-tomato-after-2.jpg" alt="Tomato after" class="photo">
          <div class="photo-caption">Full plant after all work</div>
        </div>
        <div class="photo-container">
          <img src="sample-tomato-after-3.jpg" alt="Tomato after" class="photo">
          <div class="photo-caption">Mulch layer settled</div>
        </div>
      </div>
    </div>

    <div class="stake">
      <div class="stake-title">Stake 2 — Zucchini (direct-sown) + Green Beans <span class="time-badge">3:35 PM</span></div>
      <ul>
        <li><strong>Soil Mix:</strong> Topsoil + sand</li>
        <li><strong>Soil Moisture:</strong> Top slightly dry, moist 1 inch down</li>
        <li><strong>Current Stage:</strong> Early seedling</li>
        <li><strong>Next Stage:</strong> Vegetative growth</li>
        <li><strong>Observations:</strong> Zucchini seedling upright with firm cotyledons, first true leaf expanding. Color brightening since morning. Green bean seed still below surface.</li>
        <li><strong>Actions Taken:</strong>
          <ul style="margin-top: 4px;">
            <li style="margin-left: 20px;">Watered ½-¾ cup in morning</li>
            <li style="margin-left: 20px;">Wrapped in blanket overnight</li>
          </ul>
        </li>
      </ul>

      <div class="photo-row">
        <div class="photo-container">
          <img src="sample-zucchini-stake2-1.jpg" alt="Zucchini Stake 2" class="photo">
          <div class="photo-caption">Young seedling recovering</div>
        </div>
      </div>
    </div>

    <div class="stake">
      <div class="stake-title">Stake 3 — Zucchini (direct-sown) <span class="time-badge">2:45 PM</span></div>
      <ul>
        <li><strong>Soil Mix:</strong> Topsoil + sand</li>
        <li><strong>Soil Moisture:</strong> moist after ½ cup watering</li>
        <li><strong>Current Stage:</strong> Vegetative growth</li>
        <li><strong>Next Stage:</strong> Continued growth</li>
        <li><strong>Observations:</strong> Plant healthy and upright with new inner growth. Lower leaves show small chew marks (likely beetles or caterpillars). Stem sturdy and green.</li>
        <li><strong>Actions Taken:</strong>
          <ul style="margin-top: 4px;">
            <li style="margin-left: 20px;">Watered ½ cup at base</li>
            <li style="margin-left: 20px;">Cleaned leaves with room-temperature water</li>
            <li style="margin-left: 20px;">Applied Captain Jack's Neem Oil spray (first treatment)</li>
            <li style="margin-left: 20px;">Wrapped in blanket overnight</li>
          </ul>
        </li>
        <li><strong>Notes:</strong> Wait 1 week before mulching. First neem treatment for this plant.</li>
      </ul>

      <div class="qa-section-header"><span class='emoji'>❓</span>Questions &amp; Answers</div>
      <div class="qa-item">
        <div class="qa-question">Q: Should I clean the leaves with alcohol or water before neem oil?</div>
        <div class="qa-answer">A: Use water, not alcohol. Zucchini leaves are tender and alcohol can damage their protective coating. Use room-temp water, let dry 30min-1hr, then apply neem.</div>
      </div>

      <div class="photo-row">
        <div class="photo-container">
          <img src="sample-zucchini-stake3-1.jpg" alt="Zucchini Stake 3" class="photo">
          <div class="photo-caption">Chew marks on lower leaves</div>
        </div>
        <div class="photo-container">
          <img src="sample-zucchini-stake3-2.jpg" alt="Zucchini Stake 3" class="photo">
          <div class="photo-caption">Full plant before neem treatment</div>
        </div>
      </div>
    </div>

    <div class="stake">
      <div class="stake-title">Stake 4 — Zucchini (transplanted) <span class="time-badge">2:45 PM</span></div>
      <ul>
        <li><strong>Soil Mix:</strong> Topsoil + sand</li>
        <li><strong>Soil Moisture:</strong> barely moist</li>
        <li><strong>Current Stage:</strong> Post-transplant recovery</li>
        <li><strong>Next Stage:</strong> Vegetative growth</li>
        <li><strong>Observations:</strong> Recovering steadily. Healthy central growth and firm stems. Pale leaf color shows still re-establishing roots.</li>
        <li><strong>Actions Taken:</strong>
          <ul style="margin-top: 4px;">
            <li style="margin-left: 20px;">Watered ½-¾ cup to moisten top 2 inches</li>
            <li style="margin-left: 20px;">Applied Captain Jack's Neem Oil spray as preventive</li>
            <li style="margin-left: 20px;">Wrapped in blanket overnight</li>
          </ul>
        </li>
        <li><strong>Notes:</strong> Watch for darker leaves in 3-4 days (sign of re-anchored roots).</li>
      </ul>

      <div class="photo-row">
        <div class="photo-container">
          <img src="sample-zucchini-stake4-1.jpg" alt="Zucchini Stake 4" class="photo">
          <div class="photo-caption">Pale growth recovering</div>
        </div>
        <div class="photo-container">
          <img src="sample-zucchini-stake4-2.jpg" alt="Zucchini Stake 4" class="photo">
          <div class="photo-caption">New central growth</div>
        </div>
      </div>
    </div>

  </main>
</body>

</html>'''

    with open('templates/samples/sample_daily_journal.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("✓ Created file: templates/samples/sample_daily_journal.html (Version 13)")


def main():
    """Main setup function"""
    print("=" * 65)
    print("🌿 Garden Journal Template Setup")
    print("VERSION: 13")
    print("=" * 65)
    print()

    try:
        # Make sure directories exist
        Path('templates').mkdir(exist_ok=True)
        Path('templates/samples').mkdir(exist_ok=True)
        print("✓ Verified directory: templates/")
        print("✓ Verified directory: templates/samples/\n")

        # Create CSS file
        print("Creating CSS file...")
        create_base_css()
        print()

        # Create template files
        print("Creating template files...")
        create_daily_journal_template()
        create_sample_html()
        print()

        print("=" * 65)
        print("✅ Template setup complete! (VERSION 13)")
        print("=" * 65)
        print()
        print("📁 Files created:")
        print("  templates/base.css (Version 13)")
        print("  templates/daily_journal_template.html (Version 13)")
        print("  templates/samples/sample_daily_journal.html (Version 13)")
        print()
        print("📋 Version 13 Major Features:")
        print("  ✓ Multiple observations per plant per day with time badges")
        print("  ✓ Photo captions and metadata support")
        print("  ✓ Soil moisture field display")
        print("  ✓ Detailed actions with nested lists (amounts/products)")
        print("  ✓ Upcoming Actions section")
        print("  ✓ Container grouping (stakes and positions)")
        print("  ✓ Shared container support (Arugula/Cilantro example)")
        print("  ✓ Print CSS removed (use Print Friendly & PDF plugin)")
        print("  ✓ Samples in templates/samples/ folder")
        print()
        print("📷 Sample photos needed in templates/samples/ folder:")
        print("  Basil: sample-basil-left-1.jpg, -2.jpg, sample-basil-right-1.jpg")
        print("  Strawberry Left: sample-strawberry-left-1.jpg, -2.jpg, -3.jpg")
        print("  Strawberry Right: sample-strawberry-right-before-1.jpg,")
        print("                    sample-strawberry-right-1.jpg,")
        print("                    sample-strawberry-right-after-1.jpg")
        print("  Greens: sample-arugula-1.jpg, sample-cilantro-1.jpg")
        print("  Tomato: sample-tomato-before-1.jpg through -4.jpg")
        print("          sample-tomato-after-1.jpg through -3.jpg")
        print("  Zucchini: sample-zucchini-stake2-1.jpg,")
        print("            sample-zucchini-stake3-1.jpg, -2.jpg,")
        print("            sample-zucchini-stake4-1.jpg, -2.jpg")
        print()
        print("🎯 Next steps:")
        print("  1. Add sample photos to templates/samples/ folder")
        print("  2. Open templates/samples/sample_daily_journal.html in browser")
        print("  3. Review layout with real Nov 11 data!")
        print("  4. Add 'templates/samples/' to .gitignore")
        print("\n🌱 Happy gardening!")

    except Exception as e:
        print(f"\n❌ Error during setup: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())