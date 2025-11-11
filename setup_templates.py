#!/usr/bin/env python3
"""
Garden Journal Template Setup Script

This script creates the CSS file and HTML templates for the garden journal.

Usage:
    python setup_templates.py
"""

import os
from pathlib import Path


def create_base_css():
    """Create templates/base.css with all shared styles"""
    content = """/* Garden Journal Base Styles */

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
  font-size: 16px;
  margin: 12px 0 6px;
  color: var(--text);
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
}

.photo {
  width: 2.0in;
  height: 1.5in;
  border-radius: 10px;
  object-fit: cover;
  border: 1px solid var(--rule);
}

/* Hide empty photo slots */
.photo-slot {
  display: none;
}

/* Print Styles */
@media print {
  @page {
    size: 8.5in 11in;
    margin: 0.25in;
  }

  body {
    font-size: 11pt;
  }

  .divider {
    page-break-after: avoid;
  }

  .panel,
  .stake {
    page-break-inside: avoid;
  }
}
"""

    with open('templates/base.css', 'w', encoding='utf-8') as f:
        f.write(content)
    print("✓ Created file: templates/base.css")


def create_daily_journal_template():
    """Create templates/daily_journal_template.html"""
    content = '''<!doctype html>
<html lang="en">

<head>
  <meta charset="utf-8">
  <title>Daily Journal — {{ date }}</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="styles.css">
</head>

<body>
  <main>

    <h1><span class='emoji'>🌿</span>Daily Journal</h1>
    <p class="note">Date: {{ formatted_date }} • Panels 1–18 (left → right); Stakes 1–4 within the raised bed</p>
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
    <p class="lead">
      {% if weather.temp_high and weather.temp_low %}
      <strong>Temperature:</strong> {{ weather.temp_low }}°F – {{ weather.temp_high }}°F<br>
      {% endif %}
      {% if weather.conditions %}
      <strong>Conditions:</strong> {{ weather.conditions }}<br>
      {% endif %}
      {% if weather.sunrise and weather.sunset %}
      <strong>Sun:</strong> Sunrise {{ weather.sunrise }}, Sunset {{ weather.sunset }}<br>
      {% endif %}
      {% if weather.humidity %}
      <strong>Humidity:</strong> {{ weather.humidity }}%<br>
      {% endif %}
      {% if weather.wind %}
      <strong>Wind:</strong> {{ weather.wind }}<br>
      {% endif %}
      {% if weather.notes %}
      <strong>Notes:</strong> {{ weather.notes }}
      {% endif %}
    </p>
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

    <hr class="divider" />

    <!-- PLANT BY PLANT -->
    <h2 style="font-size: 22px; margin-top: 32px;"><span class='emoji'>🪴</span>Plant by Plant</h2>
    <p class="note">Each entry lists container and care notes, followed by photos (if available)</p>

    {% for plant in plant_observations %}

    <!-- Check if this is a raised bed plant (contains "Stake" in location) -->
    {% if "Stake" in plant.location %}

      <!-- If this is the first stake, add raised bed header -->
      {% if loop.index == 1 or "Stake" not in plant_observations[loop.index-2].location %}
      <h3><span class='emoji'>🥕</span>Raised Bed — Panels 16–18</h3>
      {% endif %}

      <div class="stake">
        <div class="stake-title">{{ plant.location }} — {{ plant.plant_id|replace('_', ' ')|title }}</div>
        <ul>
          <li><strong>Soil Mix:</strong> {{ plant.soil_mix }}</li>
          <li><strong>Current Stage:</strong> {{ plant.current_stage }}</li>
          <li><strong>Next Stage:</strong> {{ plant.next_stage }}</li>
          <li><strong>Notes:</strong> {{ plant.notes }}</li>
        </ul>

        {% if plant.plant_qa %}
        <div class="qa-item">
          <div class="qa-question">Q: {{ plant.plant_qa.question }}</div>
          <div class="qa-answer">A: {{ plant.plant_qa.answer }}</div>
        </div>
        {% endif %}

        {% if plant.photos and plant.photos|length > 0 %}
        <div class="photo-row">
          {% for photo in plant.photos[:4] %}
          <img src="../photos/{{ photo }}" alt="{{ plant.plant_id }}" class="photo">
          {% endfor %}
        </div>
        {% endif %}
      </div>

    {% else %}
      <!-- Regular panel plant -->
      <div class="panel">
        <div class="panel-title">{{ plant.location }}</div>
        <ul>
          <li><strong>Container:</strong> {{ plant.container }}</li>
          <li><strong>Soil Mix:</strong> {{ plant.soil_mix }}</li>
          <li><strong>Current Stage:</strong> {{ plant.current_stage }}</li>
          <li><strong>Next Stage:</strong> {{ plant.next_stage }}</li>
          <li><strong>Notes:</strong> {{ plant.notes }}</li>
        </ul>

        {% if plant.plant_qa %}
        <div class="qa-item">
          <div class="qa-question">Q: {{ plant.plant_qa.question }}</div>
          <div class="qa-answer">A: {{ plant.plant_qa.answer }}</div>
        </div>
        {% endif %}

        {% if plant.photos and plant.photos|length > 0 %}
        <div class="photo-row">
          {% for photo in plant.photos[:4] %}
          <img src="../photos/{{ photo }}" alt="{{ plant.plant_id }}" class="photo">
          {% endfor %}
        </div>
        {% endif %}
      </div>

      <hr class="divider" />
    {% endif %}

    {% endfor %}

  </main>
</body>

</html>'''

    with open('templates/daily_journal_template.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("✓ Created file: templates/daily_journal_template.html")


def create_sample_html():
    """Create a sample HTML file to preview the template"""
    content = '''<!doctype html>
<html lang="en">

<head>
  <meta charset="utf-8">
  <title>Daily Journal — November 7, 2025</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="base.css">
</head>

<body>
  <main>

    <h1><span class='emoji'>🌿</span>Daily Journal</h1>
    <p class="note">Date: Friday, November 7, 2025 • Panels 1–18 (left → right); Stakes 1–4 within the raised bed</p>
    <hr class="divider" />

    <!-- SUMMARY OF ACTIVITIES -->
    <h2><span class='emoji'>📝</span>Summary of Activities</h2>
    <ul>
      <li>Morning inspection of all plants</li>
      <li>Watered basil and strawberry plants</li>
      <li>Photographed all panels and stakes</li>
    </ul>

    <!-- WEATHER / SUN CONDITIONS -->
    <h2><span class='emoji'>☀️</span>Weather / Sun Conditions</h2>
    <ul>
      <li><strong>Temperature:</strong> 58°F – 75°F</li>
      <li><strong>Conditions:</strong> Sunny and clear</li>
      <li><strong>Sun:</strong> Sunrise 0653, Sunset 1745</li>
      <li><strong>Notes:</strong> Panels 1-4 in partial shade until 8am</li>
    </ul>

    <!-- GENERAL OBSERVATIONS -->
    <h2><span class='emoji'>📝</span>General Observations</h2>
    <ul>
      <li>All plants looking healthy</li>
      <li>Soil moisture good across all containers</li>
      <li>No pest activity visible</li>
    </ul>

    <!-- QUESTIONS & ANSWERS (GENERAL) -->
    <h2><span class='emoji'>❓</span>Questions &amp; Answers</h2>
    <div class="qa-item">
      <div class="qa-question">Q: Should I start fertilizing the tomato plant?</div>
      <div class="qa-answer">A: Wait until you see the first flowers forming, then start with a diluted 10-10-10 fertilizer at half strength every 2 weeks.</div>
    </div>

    <hr class="divider" />

    <!-- PLANT BY PLANT -->
    <h2><span class='emoji'>🪴</span>Plant by Plant</h2>
    <p class="note">Each entry lists container and care notes, followed by photos (if available)</p>

    <!-- Panel 1 - Basil -->
    <div class="panel">
      <div class="panel-title">Panel 1 — Basil Left</div>
      <ul>
        <li><strong>Container:</strong> 8" white round pot, 0.94 gal</li>
        <li><strong>Soil Mix:</strong> Miracle-Gro Moisture Control</li>
        <li><strong>Current Stage:</strong> Vegetative growth</li>
        <li><strong>Next Stage:</strong> Ready for harvest</li>
        <li><strong>Notes:</strong> Healthy, compact growth. No issues observed.</li>
      </ul>

      <div class="photo-row">
        <img src="sample-basil-1.jpg" alt="Basil" class="photo">
        <img src="sample-basil-2.jpg" alt="Basil" class="photo">
      </div>
    </div>

    <hr class="divider" />

    <!-- Panel 4 - Strawberry -->
    <div class="panel">
      <div class="panel-title">Panel 4 — Strawberry Original</div>
      <ul>
        <li><strong>Container:</strong> 2.32 qt black pot</li>
        <li><strong>Soil Mix:</strong> Original potting soil + topsoil fill</li>
        <li><strong>Current Stage:</strong> Flowering</li>
        <li><strong>Next Stage:</strong> Fruit development</li>
        <li><strong>Notes:</strong> Multiple blooms present. Plant responding well to larger pot.</li>
      </ul>

      <div class="qa-item">
        <div class="qa-question">Q: How many flowers should I keep?</div>
        <div class="qa-answer">A: For a young plant, keep 2-3 of the strongest blooms. Remove weaker flowers so the plant focuses energy on fewer, larger berries.</div>
      </div>

      <div class="photo-row">
        <img src="sample-strawberry-1.jpg" alt="Strawberry" class="photo">
        <img src="sample-strawberry-2.jpg" alt="Strawberry" class="photo">
        <img src="sample-strawberry-3.jpg" alt="Strawberry" class="photo">
      </div>

    <!-- Raised Bed Section -->
    <h3><span class='emoji'>🥕</span>Raised Bed — Panels 16–18</h3>

    <div class="stake">
      <div class="stake-title">Stake 1 — Cherry Tomato</div>
      <ul>
        <li><strong>Soil Mix:</strong> Topsoil + sand</li>
        <li><strong>Current Stage:</strong> Early flowering</li>
        <li><strong>Next Stage:</strong> Fruit set</li>
        <li><strong>Notes:</strong> Multiple flower clusters visible. Healthy green foliage. Tied to stake.</li>
      </ul>

      <div class="photo-row">
        <img src="sample-tomato-1.jpg" alt="Tomato" class="photo">
      </div>
    </div>

    <div class="stake">
      <div class="stake-title">Stake 3 — Zucchini (direct-sown)</div>
      <ul>
        <li><strong>Soil Mix:</strong> Topsoil + sand</li>
        <li><strong>Current Stage:</strong> Vegetative growth</li>
        <li><strong>Next Stage:</strong> Continued growth</li>
        <li><strong>Notes:</strong> Largest direct-sown zucchini. Steady growth, healthy leaves.</li>
      </ul>

      <div class="photo-row">
        <img src="sample-zucchini-1.jpg" alt="Zucchini" class="photo">
        <img src="sample-zucchini-2.jpg" alt="Zucchini" class="photo">
        <img src="sample-zucchini-3.jpg" alt="Zucchini" class="photo">
        <img src="sample-zucchini-4.jpg" alt="Zucchini" class="photo">
      </div>
    </div>

  </main>
</body>

</html>'''

    with open('templates/sample_daily_journal.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("✓ Created file: templates/sample_daily_journal.html")


def main():
    """Main setup function"""
    print("🌿 Setting up Garden Journal Templates...\n")

    try:
        # Make sure templates directory exists
        Path('templates').mkdir(exist_ok=True)
        print("✓ Verified directory: templates/\n")

        # Create CSS file
        print("Creating CSS file...")
        create_base_css()
        print()

        # Create template files
        print("Creating template files...")
        create_daily_journal_template()
        create_sample_html()
        print()

        print("✅ Template setup complete!\n")
        print("📁 Files created:")
        print("  templates/base.css")
        print("  templates/daily_journal_template.html")
        print("  templates/sample_daily_journal.html")
        print()
        print("🎯 Next steps:")
        print("  1. Open templates/sample_daily_journal.html in your browser")
        print("  2. Review the styling and layout")
        print("  3. Let me know if you want any changes!")
        print("\n🌱 Happy gardening!")

    except Exception as e:
        print(f"\n❌ Error during setup: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())