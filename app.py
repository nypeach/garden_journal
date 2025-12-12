"""
Master Garden Dashboard - Flask Application
Simple, self-hosted web application for garden management
"""

from flask import Flask, render_template, jsonify, request, flash, redirect, url_for
import os
from pathlib import Path
from datetime import datetime
from data_manager import DataManager
from PIL import Image
import io

# Register HEIC support
try:
    from pillow_heif import register_heif_opener
    register_heif_opener()
except ImportError:
    print("Warning: pillow-heif not installed. HEIC files will not be supported.")
    print("Install with: pip3 install pillow-heif")

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'  # Change this in production
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size

# Photo storage configuration
PHOTO_BASE_PATH = Path('/Users/jodisilverman/Library/CloudStorage/GoogleDrive-jodimsilverman@gmail.com/My Drive/Garden Photos')
COMPRESSION_QUALITY = 85  # JPEG quality percentage

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


@app.route('/photo-prep', methods=['GET', 'POST'])
def photo_prep():
    """
    Photo Prep Tool - Prepare photos for ChatGPT plant channels
    Handles photo upload, compression, renaming, and organization
    """
    if request.method == 'GET':
        # Show the form
        return render_template('photo_prep.html', current_date=datetime.now().strftime('%Y-%m-%d'))

    # POST - Process photos
    try:
        # Get form data
        plant_id = request.form.get('plant_id', '').strip()
        date_str = request.form.get('date', '')
        starting_number = request.form.get('starting_number', '').strip()
        context = request.form.get('context', 'Initial')
        message = request.form.get('message', '').strip()
        files = request.files.getlist('photos')

        # Validation
        if not plant_id:
            flash('Plant ID is required', 'error')
            return redirect(url_for('photo_prep'))

        if not files or files[0].filename == '':
            flash('At least one photo is required', 'error')
            return redirect(url_for('photo_prep'))

        if not date_str:
            flash('Date is required', 'error')
            return redirect(url_for('photo_prep'))

        # Parse date and create filename date format (YYYYMMDD)
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        date_filename = date_obj.strftime('%Y%m%d')

        # Determine starting number
        start_num = 1
        if starting_number:
            try:
                start_num = int(starting_number)
            except ValueError:
                flash('Starting number must be a valid number', 'error')
                return redirect(url_for('photo_prep'))

        # Create plant subfolder if it doesn't exist
        plant_folder = PHOTO_BASE_PATH / plant_id
        plant_folder.mkdir(parents=True, exist_ok=True)

        # Process each photo
        processed_files = []
        current_num = start_num

        for file in files:
            if file.filename:
                try:
                    # Generate new filename
                    new_filename = f"{plant_id}-{date_filename}-{current_num:02d}.jpeg"
                    file_path = plant_folder / new_filename

                    # Save uploaded file to temporary location first
                    temp_path = plant_folder / f"temp_{file.filename}"
                    file.save(temp_path)

                    # Open and compress image
                    img = Image.open(temp_path)

                    # Convert RGBA to RGB if necessary (for PNG with transparency)
                    if img.mode in ('RGBA', 'LA', 'P'):
                        background = Image.new('RGB', img.size, (255, 255, 255))
                        if img.mode == 'P':
                            img = img.convert('RGBA')
                        background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                        img = background
                    elif img.mode != 'RGB':
                        img = img.convert('RGB')

                    # Save with compression
                    img.save(
                        file_path,
                        'JPEG',
                        quality=COMPRESSION_QUALITY,
                        optimize=True,
                        progressive=True
                    )

                    # Delete temporary file
                    temp_path.unlink()

                    processed_files.append(new_filename)
                    current_num += 1

                except Exception as img_error:
                    print(f"Error processing {file.filename}: {str(img_error)}")
                    print(f"File type: {type(file)}, Stream type: {type(file.stream)}")
                    import traceback
                    traceback.print_exc()
                    # Clean up temp file if it exists
                    if 'temp_path' in locals() and temp_path.exists():
                        temp_path.unlink()
                    raise

        # Generate output message
        output_lines = []
        if message:
            output_lines.append(message)
            output_lines.append('')  # Blank line

        # Add instruction block
        output_lines.append('Also, instead of the "<<put filename here>>" literal, please use these photo names instead. I\'ve numbered them according to how I uploaded them. Never save probe reading photos.')
        output_lines.append('')  # Blank line

        output_lines.append('Here are the photo names:')
        for idx, filename in enumerate(processed_files, 1):
            # Add probe warning only for first photo if it ends in -01
            if idx == 1 and filename.endswith('-01.jpeg'):
                output_lines.append(f'{idx}. {filename}  **Do not import if probe reading**')
            else:
                output_lines.append(f'{idx}. {filename}')

        output_message = '\n'.join(output_lines)

        # Render success page with output
        return render_template(
            'photo_prep.html',
            success=True,
            output_message=output_message,
            processed_count=len(processed_files),
            plant_folder=str(plant_folder),
            current_date=datetime.now().strftime('%Y-%m-%d')
        )

    except Exception as e:
        flash(f'Error processing photos: {str(e)}', 'error')
        return redirect(url_for('photo_prep'))


@app.route('/photos/<plant_id>/<filename>')
def serve_photo(plant_id, filename):
    """
    Serve photos from Google Drive folder
    Photos are organized in plant-specific subfolders
    """
    try:
        from flask import send_from_directory
        photo_folder = PHOTO_BASE_PATH / plant_id
        return send_from_directory(photo_folder, filename)
    except Exception as e:
        # Return 404 if photo not found
        return f"Photo not found: {filename}", 404


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