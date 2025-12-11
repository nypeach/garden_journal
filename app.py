"""
Master Garden Dashboard - Flask Application
Simple, self-hosted web application for garden management
"""

from flask import Flask, render_template, jsonify
import os
from pathlib import Path
from datetime import datetime
from data_manager import DataManager

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'  # Change this in production

# Initialize data manager
data_dir = Path(__file__).parent / 'data'
data_manager = DataManager(data_dir)

# Emoji mapping for plant categories
PLANT_EMOJIS = {
    'strawberry': '🍓',
    'broccoli': '🥦',
    'green_bean': '🫛',
    'pepper': '🌶️',
    'tomato': '🍅',
    'zucchini': '🥒',
    'shallot': '🧅',
    'garlic': '🧄',
    'scallion': '🌱',
    'chamomile': '🌼',
    'lavender': '🪻',
    'arugula': '🌿',
    'basil': '🌿',
    'chives': '🌿',
    'cilantro': '🌿',
    'oregano': '🌿',
    'parsley': '🌿',
    'parlsey': '🌿',  # Handle typo in data
    'thyme': '🌿',
    'mum': '🌸'
}

def get_plant_emoji(plant_id):
    """Get emoji for a plant based on its ID"""
    # Extract plant type from ID (e.g., 'strawberry_001' -> 'strawberry')
    plant_type = plant_id.rsplit('_', 1)[0]
    return PLANT_EMOJIS.get(plant_type, '🌱')

@app.route('/')
def index():
    """
    Home route - Master Garden Dashboard
    Displays all plants organized by categories from dashboard_order.json
    """
    try:
        # Load plants ordered by dashboard_order.json
        categories = data_manager.get_ordered_plants()

        # Get metadata for garden name
        metadata = data_manager.get_metadata()
        garden_name = metadata.get('garden_name', 'Master Garden Dashboard')

        # Get current date in readable format
        current_date = datetime.now().strftime('%B %d, %Y')

        return render_template(
            'dashboard.html',
            categories=categories,
            garden_name=garden_name,
            current_date=current_date
        )
    except Exception as e:
        return f"Error loading dashboard: {str(e)}", 500


@app.route('/journal/<plant_id>')
def journal(plant_id):
    """
    Journal route - Display plant journal with all entries
    """
    try:
        # Load full plant data
        plant = data_manager.get_plant(plant_id)

        if not plant:
            return f"Plant {plant_id} not found", 404

        # Extract data for template
        plant_name = plant.get('plant', 'Unknown Plant')
        plant_emoji = get_plant_emoji(plant_id)
        journal_entries = plant.get('journal', [])
        current_state = plant.get('current_state', '')
        current_stage = plant.get('current_stage', '')

        return render_template(
            'journal.html',
            plant_name=plant_name,
            plant_emoji=plant_emoji,
            journal=journal_entries,
            plant_id=plant_id,
            current_state=current_state,
            current_stage=current_stage
        )
    except Exception as e:
        return f"Error loading journal: {str(e)}", 500


@app.route('/api/plant/<plant_id>')
def get_plant(plant_id):
    """
    API endpoint to get full plant data by ID
    Returns JSON for use in modals or other dynamic content
    """
    try:
        plant = data_manager.get_plant(plant_id)
        if plant:
            return jsonify(plant)
        else:
            return jsonify({'error': 'Plant not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/plants')
def get_all_plants():
    """
    API endpoint to get all plants
    Returns JSON array of all plant data
    """
    try:
        plants = data_manager.get_all_plants()
        return jsonify(plants)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/health')
def health_check():
    """
    Health check endpoint
    Returns OK if server is running
    """
    return jsonify({'status': 'OK'})


if __name__ == '__main__':
    # Run the Flask development server
    # Access at http://localhost:3000
    app.run(host='0.0.0.0', port=3000, debug=True)