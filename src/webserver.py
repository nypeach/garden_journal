#!/usr/bin/env python3
"""
=================================================================
Garden Journal Web Server
VERSION: 1.0
Last Updated: 2025-11-13
=================================================================

Flask web server for garden journal forms.
Serves HTML forms and handles form submissions.

Usage:
    python3 src/web_server.py

Then open browser to: http://localhost:3000
"""

from flask import Flask, render_template, request, jsonify, send_from_directory
from pathlib import Path
import sys
import base64
# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent))

# Import data manager functions
from data_manager import (
    load_data,
    add_plant,
    move_plant,
    add_daily_entry,
    get_all_plants,
    get_plant_by_id
)

# Import HTML generator
from html_generator import GardenHTMLGenerator

app = Flask(__name__,
            template_folder='../forms',
            static_folder='../forms/static')

# Configuration
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size

@app.route('/')
def index():
    """Landing page with navigation and stats"""
    try:
        data = load_data()

        # Calculate stats
        total_plants = len([p for p in data.get('plants', []) if p.get('status') == 'active'])

        # Get last entry date
        daily_entries = data.get('daily_entries', [])
        last_entry_date = None
        if daily_entries:
            dates = [entry.get('date') for entry in daily_entries if entry.get('date')]
            if dates:
                last_entry_date = max(dates)

        return render_template('index.html',
                             total_plants=total_plants,
                             last_entry_date=last_entry_date)
    except Exception as e:
        print(f"Error loading index: {e}")
        return render_template('index.html',
                             total_plants=0,
                             last_entry_date=None,
                             error=str(e))


@app.route('/add-plant')
def add_plant_form():
    """Render add plant form"""
    return render_template('add_plant.html')


@app.route('/add-entry')
def add_entry_form():
    """Render daily entry form"""
    try:
        data = load_data()
        plants = [p for p in data.get('plants', []) if p.get('status') == 'active']
        return render_template('add_entry.html', plants=plants)
    except Exception as e:
        print(f"Error loading add entry form: {e}")
        return render_template('add_entry.html', plants=[], error=str(e))


@app.route('/move-plant')
def move_plant_form():
    """Render move plant form"""
    try:
        data = load_data()
        plants = [p for p in data.get('plants', []) if p.get('status') == 'active']
        return render_template('move_plant.html', plants=plants)
    except Exception as e:
        print(f"Error loading move plant form: {e}")
        return render_template('move_plant.html', plants=[], error=str(e))


# API Routes (will be implemented as we build each form)

@app.route('/api/plants', methods=['GET'])
def api_get_plants():
    """Get list of all active plants"""
    try:
        plants = get_all_plants()
        active_plants = [p for p in plants if p.get('status') == 'active']
        return jsonify({'success': True, 'plants': active_plants})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/plant/<plant_id>', methods=['GET'])
def api_get_plant(plant_id):
    """Get single plant data"""
    try:
        plant = get_plant_by_id(plant_id)
        if plant:
            return jsonify({'success': True, 'plant': plant})
        else:
            return jsonify({'success': False, 'error': 'Plant not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/output/<path:filename>')
def serve_output(filename):
    """Serve generated HTML files from output folder"""
    output_dir = Path(__file__).parent.parent / 'output'
    response = send_from_directory(output_dir, filename)

    # Prevent browser caching of generated HTML files
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'

    return response


@app.route('/api/add-plant', methods=['POST'])
def api_add_plant():
    """Add a new plant"""
    try:
        data = request.get_json()

        # Get existing plants to generate new plant_id
        existing_plants = get_all_plants()
        existing_ids = [p['plant_id'] for p in existing_plants]

        # Generate plant_id
        from schema import generate_plant_id
        plant_id = generate_plant_id(data['plant_type'], existing_ids)

        # Call data_manager to add plant (returns None on success, raises on error)
        add_plant(
            plant_id=plant_id,
            plant_type=data['plant_type'],
            common_name=data['common_name'],
            variety=data.get('variety'),
            purchase_date=data['purchase_date'],
            location=data['location'],
            container_type=data['container_type'],
            container_name=data['container_name'],
            soil_mix=data['soil_mix'],
            container_size=data.get('container_size'),
            stake_number=data.get('stake_number'),
            position=data.get('position'),
            summary=data.get('summary')
        )

        # Regenerate static pages to show new plant
        generator = GardenHTMLGenerator()
        if generator.load_data():
            generator.setup_output_dir()
            generator.generate_front_page()
            generator.generate_layout_page()
            generator.generate_plant_summary()

        # Get the newly added plant to return in response
        new_plant = get_plant_by_id(plant_id)

        # If no exception was raised, it succeeded
        return jsonify({
            'success': True,
            'plant': new_plant,
            'message': 'Plant added successfully'
        })

    except Exception as e:
        print(f"Error adding plant: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/move-plant', methods=['POST'])
def api_move_plant():
    """Move a plant to a new location"""
    try:
        data = request.get_json()

        # Get plant data to show old location in response
        plant = get_plant_by_id(data['plant_id'])
        old_location = plant.get('current_location', {}).get('location', 'Unknown') if plant else 'Unknown'

        # Call data_manager to move plant (returns None on success, raises on error)
        move_plant(
            plant_id=data['plant_id'],
            date=data['move_date'],
            new_location=data['new_location'],
            container_type=data['container_type'],
            container_name=data['container_name'],
            soil_mix=data['soil_mix'],
            reason=data['reason'],
            container_size=data.get('container_size'),
            stake_number=data.get('stake_number'),
            position=data.get('position')
        )

        # Regenerate static pages to show updated location
        generator = GardenHTMLGenerator()
        if generator.load_data():
            generator.setup_output_dir()
            generator.generate_front_page()
            generator.generate_layout_page()
            generator.generate_plant_summary()

        # If no exception was raised, it succeeded
        return jsonify({
            'success': True,
            'old_location': old_location,
            'message': 'Plant moved successfully'
        })

    except Exception as e:
        print(f"Error moving plant: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# Add this to src/web_server.py
# Place it before the "if __name__ == '__main__':" line

import base64
from pathlib import Path

@app.route('/api/add-entry', methods=['POST'])
def api_add_entry():
    """Add a new daily entry with photos"""
    try:
        data = request.get_json()

        # Parse markdown bullets into arrays
        activities = parse_markdown_bullets(data.get('activities', ''))
        observations_text = data.get('observations', '')

        # Process plant observations
        plant_observations = []
        for obs_data in data.get('plant_observations', []):
            # Handle status changes
            if obs_data.get('status_changed') and obs_data.get('status_reason'):
                # Update plant status
                plant = get_plant_by_id(obs_data['plant_id'])
                if plant:
                    plant['status'] = obs_data['status']
                    plant['status_date'] = data['date']
                    plant['status_reason'] = obs_data['status_reason']
                    # Save updated plant (will need to call save_data)

            # Update plant summary if changed
            if obs_data.get('summary'):
                from data_manager import update_plant_summary
                try:
                    update_plant_summary(obs_data['plant_id'], obs_data['summary'])
                except Exception as e:
                    print(f"Warning: Could not update summary for {obs_data['plant_id']}: {e}")

            # Process and save photos
            saved_photos = []
            for photo_data in obs_data.get('photos', []):
                try:
                    # Decode base64 blob and save to photos/ folder
                    photo_filename = save_photo_from_blob(
                        photo_data['compressed_blob_base64'],
                        photo_data['filename']
                    )

                    saved_photos.append({
                        'filename': photo_filename,
                        'timestamp': photo_data.get('timestamp'),
                        'caption': photo_data.get('caption'),
                        'tags': photo_data.get('tags', [])
                    })
                except Exception as e:
                    print(f"Error saving photo {photo_data.get('filename')}: {e}")
                    continue

            # Build observation object for data_manager
            plant_obs = {
                'plant_id': obs_data['plant_id'],
                'time': obs_data['time'],
                'observation': obs_data['observations'],
                'photos': saved_photos,
                'soil_moisture': obs_data['soil'].get('moisture'),
                'care_actions': parse_markdown_bullets(obs_data.get('actions', '')),
                'plant_qa': obs_data.get('qa', []),
                'notes': obs_data.get('notes'),
                'current_stage': obs_data['growth'].get('current_stage'),
                'next_stage': obs_data['growth'].get('next_stage')
            }

            plant_observations.append(plant_obs)

        # Call data_manager to add daily entry
        add_daily_entry(
            date=data['date'],
            summary_of_activities=activities,
            weather=data['weather'],
            general_observations=observations_text,
            general_qa=data.get('qa', []),
            upcoming_actions=[{
                'description': action['description'],
                'target_date': action.get('target_date'),
                'target_timeframe': action.get('target_timeframe')
            } for action in data.get('upcoming_actions', [])],
            plant_observations=plant_observations
        )

        # Regenerate ALL pages
        generator = GardenHTMLGenerator()
        if generator.load_data():
            generator.setup_output_dir()
            generator.generate_front_page()
            generator.generate_layout_page()
            generator.generate_plant_summary()
            generator.generate_daily_journal(date=data['date'])

        # Return success with link to generated page
        return jsonify({
            'success': True,
            'date': data['date'],
            'journal_file': f"Garden_03_Daily_{data['date']}.html",
            'photos_saved': sum(len(obs.get('photos', [])) for obs in data.get('plant_observations', [])),
            'plants_observed': len(data.get('plant_observations', []))
        })

    except Exception as e:
        print(f"Error adding daily entry: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500


def parse_markdown_bullets(text):
    """Parse markdown bullet text into array of strings"""
    if not text or not text.strip():
        return []

    lines = text.strip().split('\n')
    bullets = []

    for line in lines:
        stripped = line.strip()
        if stripped.startswith('- '):
            # Remove the dash-space prefix
            bullets.append(stripped[2:])
        elif stripped:
            # Non-bullet line, keep as-is
            bullets.append(stripped)

    return bullets


def save_photo_from_blob(base64_blob, filename):
    """Save a base64-encoded blob to photos/ folder"""
    photos_dir = Path(__file__).parent.parent / 'photos'
    photos_dir.mkdir(exist_ok=True)

    # Decode base64
    photo_bytes = base64.b64decode(base64_blob)

    # Save to file
    photo_path = photos_dir / filename
    with open(photo_path, 'wb') as f:
        f.write(photo_bytes)

    print(f"✓ Saved photo: {filename}")
    return filename

@app.route('/refresh-and-view/<page_name>')
def refresh_and_view(page_name):
    """Regenerate all static pages then redirect to requested page"""
    try:
        # Regenerate all static pages
        generator = GardenHTMLGenerator()
        if generator.load_data():
            generator.setup_output_dir()
            generator.generate_front_page()
            generator.generate_layout_page()
            generator.generate_plant_summary()

        # Redirect to requested page
        from flask import redirect
        return redirect(f'/output/{page_name}')

    except Exception as e:
        print(f"Error regenerating pages: {e}")
        return f"Error: {e}", 500


if __name__ == '__main__':
    print("=" * 70)
    print("🌿 Garden Journal Web Server")
    print("=" * 70)
    print()
    print("Starting server on http://localhost:3000")
    print()
    print("Open your browser to: http://localhost:3000")
    print()
    print("Press Ctrl+C to stop the server")
    print("=" * 70)
    print()

    app.run(debug=True, port=3000, host='127.0.0.1')