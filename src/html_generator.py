#!/usr/bin/env python3
"""
=================================================================
Garden Journal HTML Generator
VERSION: 13
Last Updated: 2025-11-12
=================================================================

Generates HTML pages from garden_data.json using Jinja2 templates.

Outputs:
- Garden_00_Front_Page.html
- Garden_01_Layout.html
- Garden_02_Plant_by_Plant_Summary.html
- Garden_03_Daily_YYYYMMDD.html (one per date)

Usage:
    python3 src/html_generator.py
    python3 src/html_generator.py --daily-only --date 20251111
    python3 src/html_generator.py --static-only
"""

import json
import shutil
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime
from jinja2 import Environment, FileSystemLoader, select_autoescape

# Import validation and helper functions from schema
import sys
sys.path.insert(0, str(Path(__file__).parent))
from schema import (
    format_date_display,
    format_time_display,
    group_plants_by_container
)


class GardenHTMLGenerator:
    """Generate HTML pages from garden data"""

    def __init__(self, data_file: str = "data/garden_data.json"):
        self.data_file = Path(data_file)
        self.output_dir = Path("output")
        self.templates_dir = Path("templates")
        self.data = None

        # Setup Jinja2 environment
        self.env = Environment(
            loader=FileSystemLoader(self.templates_dir),
            autoescape=select_autoescape(['html', 'xml'])
        )

        # Add custom filters
        self.env.filters['format_date'] = format_date_display
        self.env.filters['format_time'] = format_time_display

    def load_data(self) -> bool:
        """Load garden data from JSON file"""
        if not self.data_file.exists():
            print(f"❌ Error: Data file not found: {self.data_file}")
            return False

        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
            print(f"✓ Loaded data from {self.data_file}")
            return True
        except json.JSONDecodeError as e:
            print(f"❌ Error parsing JSON: {e}")
            return False
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            return False

    def setup_output_dir(self):
        """Create output directory and copy CSS"""
        self.output_dir.mkdir(exist_ok=True)
        print(f"✓ Created output directory: {self.output_dir}")

        # Copy base.css to output/styles.css
        css_source = self.templates_dir / "base.css"
        css_dest = self.output_dir / "styles.css"

        if css_source.exists():
            shutil.copy2(css_source, css_dest)
            print(f"✓ Copied CSS: {css_source} → {css_dest}")
        else:
            print(f"⚠️  Warning: CSS file not found: {css_source}")

    def generate_front_page(self) -> bool:
        """Generate Garden_00_Front_Page.html"""
        try:
            template = self.env.get_template('front_page_template.html')

            # Calculate last_entry_date from daily_entries
            daily_entries = self.data.get('daily_entries', [])
            last_entry_date = None
            if daily_entries:
                # Get the most recent date
                dates = [entry.get('date') for entry in daily_entries if entry.get('date')]
                if dates:
                    last_entry_date = max(dates)

            context = {
                'metadata': {
                    **self.data.get('metadata', {}),
                    'last_entry_date': last_entry_date
                },
                'total_plants': len(self.data.get('plants', [])),
                'total_entries': len(daily_entries)
            }

            output = template.render(**context)
            output_file = self.output_dir / "Garden_00_Front_Page.html"

            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(output)

            print(f"✓ Generated: {output_file}")
            return True

        except Exception as e:
            print(f"❌ Error generating front page: {e}")
            return False

    def generate_layout_page(self) -> bool:
        """Generate Garden_01_Layout.html"""
        try:
            template = self.env.get_template('layout_template.html')

            # Get current plant locations
            plants = self.data.get('plants', [])

            # Group plants by location for display
            locations = {}
            for plant in plants:
                if plant.get('status') == 'active':
                    loc = plant.get('current_location', {}).get('location', 'Unknown')
                    if loc not in locations:
                        locations[loc] = []
                    locations[loc].append(plant)

            # Sort location names
            sorted_locations = self._sort_locations(list(locations.keys()))

            context = {
                'metadata': self.data.get('metadata', {}),
                'locations': locations,
                'sorted_locations': sorted_locations,
                'plants': plants
            }

            output = template.render(**context)
            output_file = self.output_dir / "Garden_01_Layout.html"

            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(output)

            print(f"✓ Generated: {output_file}")
            return True

        except Exception as e:
            print(f"❌ Error generating layout page: {e}")
            return False

    def generate_plant_summary(self) -> bool:
        """Generate Garden_02_Plant_by_Plant_Summary.html"""
        try:
            template = self.env.get_template('plant_summary_template.html')

            plants = self.data.get('plants', [])

            # Group plants by location for organized display
            locations = {}
            for plant in plants:
                if plant.get('status') == 'active':
                    loc = plant.get('current_location', {}).get('location', 'Unknown')
                    if loc not in locations:
                        locations[loc] = []
                    locations[loc].append(plant)

            # Sort locations (Panel 1, Panel 2, etc.)
            sorted_locations = self._sort_locations(list(locations.keys()))

            # Calculate last_entry_date from daily_entries
            daily_entries = self.data.get('daily_entries', [])
            last_entry_date = None
            if daily_entries:
                dates = [entry.get('date') for entry in daily_entries if entry.get('date')]
                if dates:
                    last_entry_date = max(dates)

            context = {
                'metadata': {
                    **self.data.get('metadata', {}),
                    'last_entry_date': last_entry_date
                },
                'locations': locations,
                'sorted_locations': sorted_locations,
                'plants': plants
            }

            output = template.render(**context)
            output_file = self.output_dir / "Garden_02_Plant_by_Plant_Summary.html"

            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(output)

            print(f"✓ Generated: {output_file}")
            return True

        except Exception as e:
            print(f"❌ Error generating plant summary: {e}")
            return False

    def generate_daily_journal(self, date: str = None) -> bool:
        """Generate daily journal page(s)"""
        try:
            template = self.env.get_template('daily_journal_template.html')
            daily_entries = self.data.get('daily_entries', [])

            if not daily_entries:
                print("⚠️  No daily entries found in data")
                return True

            # Filter by date if specified
            if date:
                daily_entries = [e for e in daily_entries if e.get('date') == date]
                if not daily_entries:
                    print(f"⚠️  No entries found for date: {date}")
                    return False

            generated_count = 0
            for entry in daily_entries:
                success = self._generate_single_daily_journal(template, entry)
                if success:
                    generated_count += 1

            print(f"✓ Generated {generated_count} daily journal page(s)")
            return True

        except Exception as e:
            print(f"❌ Error generating daily journal: {e}")
            return False

    def _generate_single_daily_journal(self, template, entry: Dict) -> bool:
        """Generate a single daily journal HTML file"""
        try:
            date = entry.get('date')
            if not date:
                print("⚠️  Entry missing date field")
                return False

            # Get plant observations and group them by container
            plant_obs = entry.get('plant_observations', [])

            # Group observations by container using schema function
            grouped_obs = self._group_observations_for_display(plant_obs)

            # Prepare context for template
            context = {
                'date': date,
                'formatted_date': format_date_display(date),
                'weather': entry.get('weather'),
                'activities': entry.get('activities', []),
                'observations': entry.get('observations', []),
                'questions_and_answers': entry.get('questions_and_answers', []),
                'upcoming_actions': entry.get('upcoming_actions', []),
                'plant_observations_grouped': grouped_obs
            }

            output = template.render(**context)
            output_file = self.output_dir / f"Garden_03_Daily_{date}.html"

            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(output)

            print(f"✓ Generated: {output_file}")
            return True

        except Exception as e:
            print(f"❌ Error generating daily journal for {entry.get('date', 'unknown')}: {e}")
            return False

    def _group_observations_for_display(self, observations: List[Dict]) -> Dict[str, List[Dict]]:
        """
        Group plant observations by container for display.
        Returns dict with keys like:
        - "Panel 1 — Basil Pot - Left" (single plant)
        - "Panel 7 — Pepper Box" (multiple plants with stakes)
        - "Raised Bed — Panels 16–18" (multiple plants with stakes)
        """
        grouped = {}

        for obs in observations:
            location = obs.get('location', 'Unknown')
            container_name = obs.get('container_name', 'Unknown Container')
            stake = obs.get('stake')

            # Create grouping key
            if stake:
                # Plants with stakes - group by location + container
                key = f"{location} — {container_name}"
            else:
                # No stake - could be single plant or shared container with positions
                # We'll group by location + container and let template handle display
                key = f"{location} — {container_name}"

            if key not in grouped:
                grouped[key] = []
            grouped[key].append(obs)

        # Sort observations within each group
        for key in grouped:
            obs_list = grouped[key]
            # If they have stakes, sort by stake number
            if obs_list[0].get('stake'):
                grouped[key] = sorted(obs_list, key=lambda x: x.get('stake', 0))

        return grouped

    def _sort_locations(self, locations: List[str]) -> List[str]:
        """Sort location names properly (Panel 1, Panel 2, ..., Panel 18, etc.)"""
        def location_sort_key(loc: str):
            # Extract panel number if it's a panel location
            if loc.startswith('Panel '):
                try:
                    num = int(loc.split()[1])
                    return (0, num)  # Panels come first, sorted by number
                except (ValueError, IndexError):
                    pass
            # Non-panel locations come after
            return (1, loc)

        return sorted(locations, key=location_sort_key)

    def generate_all(self, static_only: bool = False, daily_only: bool = False,
                    date: str = None) -> bool:
        """Generate all HTML pages"""

        if not self.load_data():
            return False

        self.setup_output_dir()

        success = True

        if not daily_only:
            print("\n📄 Generating static pages...")
            success = success and self.generate_front_page()
            success = success and self.generate_layout_page()
            success = success and self.generate_plant_summary()

        if not static_only:
            print("\n📅 Generating daily journal pages...")
            success = success and self.generate_daily_journal(date)

        return success


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description='Generate garden journal HTML pages')
    parser.add_argument('--static-only', action='store_true',
                       help='Generate only static pages (front, layout, summary)')
    parser.add_argument('--daily-only', action='store_true',
                       help='Generate only daily journal pages')
    parser.add_argument('--date', type=str,
                       help='Generate only for specific date (YYYYMMDD)')
    parser.add_argument('--data', type=str, default='data/garden_data.json',
                       help='Path to garden data JSON file')

    args = parser.parse_args()

    print("=" * 65)
    print("🌿 Garden Journal HTML Generator")
    print("VERSION: 13")
    print("=" * 65)
    print()

    generator = GardenHTMLGenerator(args.data)

    success = generator.generate_all(
        static_only=args.static_only,
        daily_only=args.daily_only,
        date=args.date
    )

    if success:
        print("\n" + "=" * 65)
        print("✅ HTML generation complete!")
        print("=" * 65)
        print(f"\n📂 Output files in: {generator.output_dir}/")
        print("\n🎯 Next steps:")
        print(f"  1. Open {generator.output_dir}/Garden_00_Front_Page.html in browser")
        print("  2. Use Print Friendly & PDF to save as PDF")
        print("\n🌱 Happy gardening!")
        return 0
    else:
        print("\n" + "=" * 65)
        print("❌ HTML generation failed - see errors above")
        print("=" * 65)
        return 1


if __name__ == "__main__":
    exit(main())