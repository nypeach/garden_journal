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
    return send_from_directory(output_dir, filename)


@app.route('/api/move-plant', methods=['POST'])
def api_move_plant():
    """Move a plant to a new location"""
    try:
        data = request.get_json()

        # Get plant data to show old location in response
        plant = get_plant_by_id(data['plant_id'])
        old_location = plant.get('current_location', {}).get('location', 'Unknown') if plant else 'Unknown'

        # Call data_manager to move plant
        success = move_plant(
            plant_id=data['plant_id'],
            new_location=data['new_location'],
            move_date=data['move_date'],
            reason=data['reason']
        )

        if success:
            return jsonify({
                'success': True,
                'old_location': old_location,
                'message': 'Plant moved successfully'
            })
        else:
            return jsonify({'success': False, 'error': 'Failed to move plant'}), 500

    except Exception as e:
        print(f"Error moving plant: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


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