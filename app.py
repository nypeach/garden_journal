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
    return jsonify({'status': 'ok', 'message': 'Master Garden Dashboard is running'})


def verify_directories():
    """
    Verify that all required directories exist
    Creates them if they don't exist
    """
    base_dir = Path(__file__).parent
    required_dirs = [
        base_dir / 'data' / 'plants',
        base_dir / 'static',
        base_dir / 'templates'
    ]

    for directory in required_dirs:
        if not directory.exists():
            directory.mkdir(parents=True, exist_ok=True)
            print(f"✓ Created directory: {directory}")
        else:
            print(f"✓ Directory exists: {directory}")


if __name__ == '__main__':
    print("=" * 60)
    print("🌿 Master Garden Dashboard")
    print("=" * 60)

    # Verify directories exist
    print("\nVerifying directory structure...")
    verify_directories()

    # Display startup info
    print("\n" + "=" * 60)
    print("Server starting on http://localhost:3000")
    print("Press CTRL+C to stop the server")
    print("=" * 60 + "\n")

    # Run the Flask development server
    app.run(host='0.0.0.0', port=3000, debug=True)