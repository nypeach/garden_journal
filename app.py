"""
Master Garden Dashboard - Flask Application
Simple, self-hosted web application for garden management
"""

from flask import Flask, render_template, jsonify, request, flash, redirect, url_for
import os
import json
from pathlib import Path
from datetime import datetime
from data_manager import DataManager
from PIL import Image
import io
import re
import requests
from bs4 import BeautifulSoup

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


@app.route('/channel-start', methods=['GET', 'POST'])
def channel_start():
    """
    Channel Start Tool - Bootstrap new ChatGPT plant channels
    Generates initialization messages, patches, and rename strings
    """
    if request.method == 'GET':
        # Get list of all plants for dropdown
        all_plants = data_manager.get_all_plants()

        return render_template(
            'channel_start.html',
            plants=all_plants
        )

    # POST - Process the action
    try:
        plant_id = request.form.get('plant_id', '').strip()
        action = request.form.get('action', '')

        if not plant_id:
            flash('Plant ID is required', 'error')
            return redirect(url_for('channel_start'))

        # Load plant data
        plant = data_manager.get_plant(plant_id)
        if not plant:
            flash(f'Plant not found: {plant_id}', 'error')
            return redirect(url_for('channel_start'))

        output_message = ""
        output_title = ""

        if action == 'start_channel':
            # Read the markdown files
            chatgpt_path = Path('chatgpt')

            # Read prompt file
            prompt_file = chatgpt_path / 'master_garden_01_ai_prompt.md'
            with open(prompt_file, 'r') as f:
                prompt_content = f.read()

            # Replace variables in prompt
            prompt_content = prompt_content.replace('{id}', plant_id)
            prompt_content = prompt_content.replace('{plant}', plant.get('plant', plant_id))

            # Read guide file
            guide_file = chatgpt_path / 'master_garden_02_ai_guide.md'
            with open(guide_file, 'r') as f:
                guide_content = f.read()

            # Read after JSON file
            after_json_file = chatgpt_path / 'master_garden_04_ai_after_json.md'
            with open(after_json_file, 'r') as f:
                after_json_content = f.read()

            # Get plant JSON
            plant_json = json.dumps(plant, indent=2, ensure_ascii=False)

            # Assemble the output
            output_lines = []
            output_lines.append(prompt_content)
            output_lines.append(guide_content)
            output_lines.append('')
            output_lines.append('Here is the **Initial Plant Data** JSON')
            output_lines.append('```json')
            output_lines.append(plant_json)
            output_lines.append('```')
            output_lines.append('')
            output_lines.append(after_json_content)

            output_message = '\n'.join(output_lines)
            output_title = f"Start Channel: {plant_id}"

        elif action == 'one_time_patch':
            # Read the one-time correction file
            chatgpt_path = Path('chatgpt')
            patch_file = chatgpt_path / 'master_garden_05_ai_one_time_correction.md'

            with open(patch_file, 'r') as f:
                output_message = f.read()

            output_title = "One-Time Patch"

        elif action == 'rename_chat':
            # Generate rename string
            output_message = f"🌿 MG: {plant_id}"
            output_title = "Rename Chat"

        # Get all plants for form reload
        all_plants = data_manager.get_all_plants()

        return render_template(
            'channel_start.html',
            plants=all_plants,
            output_message=output_message,
            output_title=output_title
        )

    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
        return redirect(url_for('channel_start'))


@app.route('/journal-update', methods=['GET', 'POST'])
def journal_update():
    """
    Journal Update Tool - Paste ChatGPT journal entries OR plant main data fragments
    Two actions: Update Journal Entry OR Update Plant Main Data
    """
    if request.method == 'GET':
        # Get list of all plants for dropdown
        all_plants = data_manager.get_all_plants()

        return render_template(
            'journal_update.html',
            plants=all_plants
        )

    # POST - Process the update
    try:
        import re

        plant_id = request.form.get('plant_id', '').strip()
        json_input = request.form.get('journal_json', '').strip()
        action = request.form.get('action', 'journal')  # 'journal' or 'plant_main'

        # Validation
        if not plant_id:
            return render_template(
                'journal_update.html',
                plants=data_manager.get_all_plants(),
                error=True,
                error_message="Plant ID is required"
            )

        if not json_input:
            return render_template(
                'journal_update.html',
                plants=data_manager.get_all_plants(),
                error=True,
                error_message="JSON input is required"
            )

        # Load plant data
        plant = data_manager.get_plant(plant_id)
        if not plant:
            return render_template(
                'journal_update.html',
                plants=data_manager.get_all_plants(),
                error=True,
                error_message=f"Plant not found: {plant_id}"
            )

        # Clean JSON (remove trailing commas and wrap fragments in braces if needed)
        cleaned_json = json_input.strip()

        # Remove trailing commas before closing braces/brackets
        cleaned_json = re.sub(r',(\s*[}\]])', r'\1', cleaned_json)

        # Remove trailing comma at the very end
        cleaned_json = re.sub(r',\s*$', '', cleaned_json)

        # If it doesn't start with { and isn't a journal entry, wrap it
        if not cleaned_json.startswith('{'):
            cleaned_json = '{' + cleaned_json + '}'
        elif cleaned_json.startswith('{') and cleaned_json.endswith(','):
            cleaned_json = cleaned_json.rstrip(',')

        # Parse the JSON
        try:
            parsed_data = json.loads(cleaned_json)
        except json.JSONDecodeError as e:
            return render_template(
                'journal_update.html',
                plants=data_manager.get_all_plants(),
                error=True,
                error_message="Invalid JSON format",
                error_details=str(e)
            )

        # Handle based on action type
        if action == 'plant_main':
            # UPDATE PLANT MAIN DATA (fragment)
            # Replace any attributes present in the fragment
            for key, value in parsed_data.items():
                if key != 'journal':  # Don't update journal this way
                    plant[key] = value

            action_type = f"Plant main data updated ({len(parsed_data)} attribute(s))"

        else:
            # UPDATE JOURNAL ENTRY (default)
            new_entry = parsed_data

            # Validate required fields
            if 'date' not in new_entry or 'time' not in new_entry:
                return render_template(
                    'journal_update.html',
                    plants=data_manager.get_all_plants(),
                    error=True,
                    error_message="Journal entry must have 'date' and 'time' fields"
                )

            entry_date = new_entry['date']
            entry_time = new_entry['time']

            # Ensure journal array exists
            if 'journal' not in plant:
                plant['journal'] = []

            # Check if entry with same date+time exists
            existing_index = None
            for i, entry in enumerate(plant['journal']):
                if entry.get('date') == entry_date and entry.get('time') == entry_time:
                    existing_index = i
                    break

            # Update or add entry
            if existing_index is not None:
                plant['journal'][existing_index] = new_entry
                action_type = "Journal entry updated (same date/time found)"
            else:
                plant['journal'].append(new_entry)
                action_type = "New journal entry added"

            # Sort journal array by date and time (newest first)
            def parse_datetime(entry):
                """Parse date and time for sorting"""
                try:
                    date_str = entry.get('date', '')
                    time_str = entry.get('time', '')
                    dt = datetime.strptime(f"{date_str} {time_str}", "%m/%d/%Y %I:%M %p")
                    return dt
                except:
                    return datetime.min

            plant['journal'].sort(key=parse_datetime, reverse=True)

        # Save updated plant data
        success = data_manager.save_plant(plant_id, plant)

        if not success:
            return render_template(
                'journal_update.html',
                plants=data_manager.get_all_plants(),
                error=True,
                error_message="Failed to save plant data"
            )

        # Show success page
        return render_template(
            'journal_update.html',
            success=True,
            plant_id=plant_id,
            plant_name=plant.get('plant', plant_id),
            entry_date=parsed_data.get('date', 'N/A') if action == 'journal' else 'N/A',
            entry_time=parsed_data.get('time', 'N/A') if action == 'journal' else 'N/A',
            action_type=action_type,
            total_entries=len(plant['journal']),
            plants=[]
        )

    except Exception as e:
        return render_template(
            'journal_update.html',
            plants=data_manager.get_all_plants(),
            error=True,
            error_message="Unexpected error occurred",
            error_details=str(e)
        )

@app.route('/photo-prep', methods=['GET', 'POST'])
def photo_prep():
    """
    Photo Prep Tool - Prepare photos for ChatGPT plant channels
    Handles photo upload, compression, renaming, and organization
    """
    if request.method == 'GET':
        # Get list of available plants for reference (exclude inactive)
        all_plants = data_manager.get_all_plants()
        available_plant_ids = sorted([p.get('id') for p in all_plants if p.get('id') and p.get('status') != 'Inactive'])

        # Get date from URL parameter or use today
        date_param = request.args.get('date', '')
        current_date = date_param if date_param else datetime.now().strftime('%Y-%m-%d')

        # Show the form
        return render_template(
            'photo_prep.html',
            current_date=current_date,
            available_plants=available_plant_ids
        )

    # POST - Process photos
    try:
        # Get form data
        plant_id = request.form.get('plant_id', '').strip()
        date_str = request.form.get('date', '')
        starting_number = request.form.get('starting_number', '').strip()
        context = request.form.get('context', 'Initial')
        global_message = request.form.get('global_message', '').strip()
        plant_message = request.form.get('plant_message', '').strip()
        files = request.files.getlist('photos')

        # Validation
        if not plant_id:
            flash('Plant ID is required', 'error')
            return redirect(url_for('photo_prep'))

        # Verify plant exists
        plant = data_manager.get_plant(plant_id)
        if not plant:
            flash(f'Plant not found: {plant_id}. Please check the Plant ID and try again.', 'error')
            return redirect(url_for('photo_prep'))

        if context == 'Initial' and (not files or files[0].filename == ''):
            flash('At least one photo is required for Initial context', 'error')
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

                    # Open and apply EXIF orientation
                    img = Image.open(temp_path)

                    # Fix orientation based on EXIF data
                    try:
                        from PIL import ImageOps
                        img = ImageOps.exif_transpose(img)
                    except Exception as exif_error:
                        print(f"Could not apply EXIF orientation: {exif_error}")

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
        import pytz
        eastern = pytz.timezone('US/Eastern')

        # Save original global message for form reload
        original_global_message = global_message

        if context == 'Follow-Up':
            # FOLLOW-UP TEMPLATE
            current_time = datetime.now(eastern).strftime('%-I:%M %p')

            output_lines.append('Follow-up (same day — this belongs in TODAY\'S existing Daily Journal Entry JSON, not a new day):')
            output_lines.append('')
            output_lines.append(f'Current time now: {current_time}')
            output_lines.append('')
            output_lines.append('Follow-up / question(s):')
            output_lines.append(plant_message if plant_message else '[your follow-up text here]')
            output_lines.append('')

            # Photo list or "No Photos"
            if processed_files:
                output_lines.append('New photo(s) to log:')
                for idx, filename in enumerate(processed_files, 1):
                    output_lines.append(f'{idx}. {filename}')
            else:
                output_lines.append('New photo(s) to log:')
                output_lines.append('"No Photos"')

            output_lines.append('')
            output_lines.append('✅ Respond naturally first:')
            output_lines.append('- Answer my question(s) directly in horticulturist voice')
            output_lines.append('- Address the new observation(s)')
            output_lines.append('- Do NOT repeat the full daily assessment, probe interpretation, weather analysis, or photo captions')
            output_lines.append('')
            output_lines.append('Then ask EXACTLY: "Want me to log that?"')
            output_lines.append('❌ If No — wait for further instructions.')
            output_lines.append('✅ If Yes — update TODAY\'S most recent Daily Journal Entry JSON already in this chat (use it as the base record) and re-issue the COMPLETE JSON (exact schema).')
            output_lines.append('')
            output_lines.append('Change NOTHING except:')
            output_lines.append(f'- append this follow-up to `follow_up` using the Current time now provided: `[{current_time}] {{summary}}`')
            output_lines.append('- update `q_and_a_summary` ONLY if this follow-up included a real question + your answer')
            if processed_files:
                output_lines.append('- append any new photos to the existing `photos` array (preserve all prior photos and order)')
            output_lines.append('')
            output_lines.append('IMPORTANT:')
            output_lines.append('- Do NOT change the Daily Journal Entry `time` field (it stays the probe time).')
            output_lines.append('- Output valid JSON only. No invented fields.')
            output_lines.append('- After responding and/or logging, continue normally using this Plant Channel\'s root context and the Master Garden Assistant Guide.')

        else:
            # INITIAL TEMPLATE (existing behavior)
            # Replace variables in global message with plant data
            def replace_variables(text, plant_data):
                """Replace {variable_name} with values from plant JSON"""
                pattern = r'\{([^}]+)\}'

                def replace_match(match):
                    var_name = match.group(1)
                    value = plant_data.get(var_name)
                    if value is None:
                        return "NO VARIABLE"
                    return str(value)

                return re.sub(pattern, replace_match, text)

            # Save original global message (with variables) for next plant
            original_global_message = global_message

            # Apply variable replacement to global message for OUTPUT only
            if global_message:
                global_message = replace_variables(global_message, plant)

            # Combine global and plant-specific messages
            combined_message = []
            if global_message:
                combined_message.append(global_message)
            if plant_message:
                combined_message.append(plant_message)

            if combined_message:
                output_lines.append('\n\n'.join(combined_message))
                output_lines.append('')  # Blank line

            output_lines.append('Here are the photo names:')
            for idx, filename in enumerate(processed_files, 1):
                # Check if this photo was marked as probe reading
                probe_checkbox = request.form.get(f'probe_reading_{idx-1}')
                if probe_checkbox:
                    output_lines.append(f'{idx}. {filename}  ← (probe reading)')
                else:
                    output_lines.append(f'{idx}. {filename}')

            # Add watering assessment prompt if checkbox is checked
            include_watering = request.form.get('include_watering')
            if include_watering:
                current_time = datetime.now(eastern).strftime('%-I:%M %p %Z')
                output_lines.append('')
                output_lines.append('')
                output_lines.append(f'It is now {current_time}.')

        output_message = '\n'.join(output_lines)
        # Render success page with output
        return render_template(
            'photo_prep.html',
            success=True,
            output_message=output_message,
            processed_count=len(processed_files),
            plant_folder=str(plant_folder),
            current_date=date_str,  # Use the date from the form, not today
            global_message=original_global_message  # Pass ORIGINAL with variables, not replaced
        )

    except Exception as e:
        # Re-render form with existing data instead of redirecting
        all_plants = data_manager.get_all_plants()
        available_plant_ids = sorted([p.get('id') for p in all_plants if p.get('id') and p.get('status') != 'Inactive'])

        return render_template(
            'photo_prep.html',
            current_date=date_str if 'date_str' in locals() else datetime.now().strftime('%Y-%m-%d'),
            available_plants=available_plant_ids,
            error=True,
            error_message=f'Error processing photos: {str(e)}',
            plant_id=plant_id if 'plant_id' in locals() else '',
            context=context if 'context' in locals() else 'Initial',
            starting_number=starting_number if 'starting_number' in locals() else '',
            global_message=global_message if 'global_message' in locals() else '',
            plant_message=plant_message if 'plant_message' in locals() else ''
        )


@app.route('/upload-placeholder-photo', methods=['POST'])
def upload_placeholder_photo():
    """
    Handle single photo upload for placeholder replacement
    Automatically determines filename from context
    """
    try:
        # Get form data
        plant_id = request.form.get('plant_id', '').strip()
        date_str = request.form.get('date', '').strip()  # Format: M/D/YYYY
        photo_index = request.form.get('photo_index', '').strip()
        file = request.files.get('photo')

        # Validation
        if not plant_id or not date_str or not photo_index or not file:
            return jsonify({'error': 'Missing required fields'}), 400

        # Parse date and create filename date format (YYYYMMDD)
        from datetime import datetime
        date_obj = datetime.strptime(date_str, '%m/%d/%Y')
        date_filename = date_obj.strftime('%Y%m%d')

        # Generate filename
        new_filename = f"{plant_id}-{date_filename}-{photo_index.zfill(2)}.jpeg"

        # Create plant subfolder if it doesn't exist
        plant_folder = PHOTO_BASE_PATH / plant_id
        plant_folder.mkdir(parents=True, exist_ok=True)
        file_path = plant_folder / new_filename

        # Save uploaded file to temporary location first
        temp_path = plant_folder / f"temp_{file.filename}"
        file.save(temp_path)

        # Open and apply EXIF orientation
        img = Image.open(temp_path)

        # Fix orientation based on EXIF data
        try:
            from PIL import ImageOps
            img = ImageOps.exif_transpose(img)
        except Exception as exif_error:
            print(f"Could not apply EXIF orientation: {exif_error}")

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

        # Update JSON file
        plant = data_manager.get_plant(plant_id)
        if not plant:
            return jsonify({'error': 'Plant not found'}), 404

        # Find the journal entry and update the photo filename
        updated = False
        for entry in plant.get('journal', []):
            if entry.get('date') == date_str:
                for photo in entry.get('photos', []):
                    if photo.get('file_name') == '<<put filename here>>':
                        photo['file_name'] = new_filename
                        updated = True
                        break
                if updated:
                    break

        if updated:
            # Save updated plant data
            data_manager.save_plant(plant_id, plant)
            return jsonify({
                'success': True,
                'filename': new_filename,
                'photo_url': f'/photos/{plant_id}/{new_filename}'
            })
        else:
            return jsonify({'error': 'Could not find placeholder to update'}), 404

    except Exception as e:
        print(f"Error uploading placeholder photo: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


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


@app.route('/assist-corrections')
def assist_corrections():
    """
    Assist Corrections - IF/THEN correction management
    Browse, search, and copy corrections for ChatGPT plant channels
    """
    try:
        # Load corrections from JSON
        corrections_file = Path(__file__).parent / 'data' / 'assist_corrections.json'

        with open(corrections_file, 'r', encoding='utf-8') as f:
            corrections_data = json.load(f)

        corrections = corrections_data.get('corrections', [])

        # Sort corrections by count (most used first)
        corrections = sorted(corrections, key=lambda x: x.get('count', 0), reverse=True)

        # Get unique categories and sub_categories for filters
        categories = sorted(set(c.get('category') for c in corrections if c.get('category')))

        # Get top 5 most used
        top_corrections = sorted(corrections, key=lambda x: x.get('count', 0), reverse=True)[:5]

        return render_template(
            'assist_corrections.html',
            corrections=corrections,
            categories=categories,
            top_corrections=top_corrections,
            schema_version=corrections_data.get('schema_version'),
            last_updated=corrections_data.get('last_updated')
        )

    except Exception as e:
        return f"Error loading corrections: {str(e)}", 500


@app.route('/api/correction/copy/<correction_id>', methods=['POST'])
def copy_correction(correction_id):
    """
    Increment count when correction is copied
    """
    try:
        corrections_file = Path(__file__).parent / 'data' / 'assist_corrections.json'

        with open(corrections_file, 'r', encoding='utf-8') as f:
            corrections_data = json.load(f)

        # Find and increment count
        for correction in corrections_data['corrections']:
            if correction['id'] == correction_id:
                correction['count'] = correction.get('count', 0) + 1
                break

        # Save updated data
        with open(corrections_file, 'w', encoding='utf-8') as f:
            json.dump(corrections_data, f, indent=2, ensure_ascii=False)

        return jsonify({'success': True, 'new_count': correction.get('count', 0)})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/correction/update/<correction_id>', methods=['POST'])
def update_correction(correction_id):
    """
    Update correction fields
    """
    try:
        corrections_file = Path(__file__).parent / 'data' / 'assist_corrections.json'

        # Get update data from request
        update_data = request.get_json()

        with open(corrections_file, 'r', encoding='utf-8') as f:
            corrections_data = json.load(f)

        # Find and update correction
        found = False
        for correction in corrections_data['corrections']:
            if correction['id'] == correction_id:
                # Update fields
                if 'trigger_if' in update_data:
                    correction['trigger_if'] = update_data['trigger_if']
                if 'response_then' in update_data:
                    correction['response_then'] = update_data['response_then']
                if 'anti_patterns' in update_data:
                    correction['anti_patterns'] = update_data['anti_patterns']
                if 'tags' in update_data:
                    correction['tags'] = update_data['tags']
                found = True
                break

        if not found:
            return jsonify({'error': 'Correction not found'}), 404

        # Save updated data
        with open(corrections_file, 'w', encoding='utf-8') as f:
            json.dump(corrections_data, f, indent=2, ensure_ascii=False)

        return jsonify({'success': True})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/correction/create', methods=['POST'])
def create_correction():
    """
    Create a new correction
    """
    try:
        corrections_file = Path(__file__).parent / 'data' / 'assist_corrections.json'

        # Get new correction data from request
        new_data = request.get_json()

        with open(corrections_file, 'r', encoding='utf-8') as f:
            corrections_data = json.load(f)

        # Generate new ID
        existing_ids = [c['id'] for c in corrections_data['corrections']]
        max_num = 0
        for existing_id in existing_ids:
            if existing_id.startswith('PROBE-FORMAT-') or existing_id.startswith('TITLE-'):
                try:
                    num = int(existing_id.split('-')[-1])
                    max_num = max(max_num, num)
                except:
                    pass

        new_id = f"TITLE-{str(max_num + 1).zfill(3)}"

        # Create new correction object
        new_correction = {
            'id': new_id,
            'title': new_data['title'],
            'category': new_data['category'],
            'sub_category': new_data['sub_category'],
            'trigger_if': new_data['trigger_if'],
            'response_then': new_data['response_then'],
            'anti_patterns': new_data.get('anti_patterns', []),
            'tags': new_data.get('tags', []),
            'include_footer': new_data.get('include_footer', True),
            'count': 0,
            'applies_when': ''
        }

        # Add to corrections list
        corrections_data['corrections'].append(new_correction)

        # Save updated data
        with open(corrections_file, 'w', encoding='utf-8') as f:
            json.dump(corrections_data, f, indent=2, ensure_ascii=False)

        return jsonify({'success': True, 'id': new_id})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/plant/<plant_id>/last-photo-number', methods=['GET'])
def get_last_photo_number(plant_id):
    """Get the last photo number from the most recent journal entry for today's date"""
    try:
        # Get date from query parameter (format: YYYY-MM-DD)
        date_str = request.args.get('date', '')

        if not date_str:
            return jsonify({'last_number': 0})

        # Convert to M/D/YYYY format for matching journal entries
        from datetime import datetime
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        journal_date = date_obj.strftime('%-m/%-d/%Y')

        plant = data_manager.get_plant(plant_id)
        if not plant or 'journal' not in plant:
            return jsonify({'last_number': 0})

        # Find journal entry matching the selected date
        matching_entry = None
        for entry in plant['journal']:
            if entry.get('date') == journal_date:
                matching_entry = entry
                break

        if not matching_entry:
            return jsonify({'error': f'No journal entry found for {journal_date}. Follow-ups must be on the same day as an existing journal entry.'}), 404

        if 'photos' not in matching_entry or len(matching_entry['photos']) == 0:
            return jsonify({'last_number': 0})

        # Get last photo filename from matching entry
        last_photo = matching_entry['photos'][-1]['file_name']

        # Extract number from filename: plantname_001-20251224-05.jpeg -> 05
        match = re.search(r'-(\d{2})\.(jpeg|jpg|png|heic)$', last_photo)
        if match:
            last_number = int(match.group(1))
            return jsonify({'last_number': last_number})

        return jsonify({'last_number': 0})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/weather/current', methods=['GET'])
def get_current_weather():
    """
    Fetch current weather forecast for Loxahatchee, FL from National Weather Service
    Returns formatted weather string with tiles and detailed forecast data
    """
    try:
        # Primary URL for Loxahatchee, FL
        primary_url = 'https://forecast.weather.gov/MapClick.php?lat=26.683680000000038&lon=-80.27976999999998'

        # Try primary URL up to 3 times
        html_content = None
        for attempt in range(3):
            try:
                response = requests.get(primary_url, timeout=10)
                if response.status_code == 200:
                    html_content = response.text
                    break
            except Exception as e:
                print(f"Primary URL attempt {attempt + 1} failed: {e}")
                if attempt == 2:  # Last attempt
                    print("Primary URL failed after 3 attempts, trying fallback...")

        # Fallback: Search within NWS site
        if not html_content:
            search_url = 'https://forecast.weather.gov/'
            for attempt in range(3):
                try:
                    # Search for Loxahatchee, FL
                    search_response = requests.get(search_url, params={'q': 'Loxahatchee, FL'}, timeout=10)
                    if search_response.status_code == 200:
                        # Parse to find the forecast link
                        soup = BeautifulSoup(search_response.text, 'html.parser')
                        # Try to find forecast link (this is simplified - may need adjustment)
                        forecast_link = soup.find('a', href=re.compile(r'MapClick\.php'))
                        if forecast_link:
                            fallback_url = 'https://forecast.weather.gov' + forecast_link['href']
                            response = requests.get(fallback_url, timeout=10)
                            if response.status_code == 200:
                                html_content = response.text
                                break
                except Exception as e:
                    print(f"Fallback attempt {attempt + 1} failed: {e}")

        # If both primary and fallback failed
        if not html_content:
            return jsonify({
                'error': True,
                'formatted_weather': 'Weather unavailable - please add manually'
            })

        # Parse the HTML
        soup = BeautifulSoup(html_content, 'html.parser')

        # Extract forecast tiles (first 3: Today, Tonight, Tomorrow)
        tombstone_container = soup.find('div', id='seven-day-forecast-container')
        if not tombstone_container:
            return jsonify({
                'error': True,
                'formatted_weather': 'Weather unavailable - please add manually'
            })

        tombstones = tombstone_container.find_all('div', class_='tombstone-container')
        if len(tombstones) < 3:
            return jsonify({
                'error': True,
                'formatted_weather': 'Weather unavailable - please add manually'
            })

        # Extract tile data
        tiles = []
        for i in range(3):
            period_name = tombstones[i].find('p', class_='period-name')
            short_desc = tombstones[i].find('p', class_='short-desc')
            temp = tombstones[i].find('p', class_='temp')

            tiles.append({
                'period': period_name.get_text(strip=True) if period_name else '',
                'condition': short_desc.get_text(strip=True) if short_desc else '',
                'temp': temp.get_text(strip=True) if temp else ''
            })

        # Extract detailed forecasts (first 3 rows)
        detailed_container = soup.find('div', id='detailed-forecast-body')
        if not detailed_container:
            return jsonify({
                'error': True,
                'formatted_weather': 'Weather unavailable - please add manually'
            })

        detailed_rows = detailed_container.find_all('div', class_='row')[:3]
        detailed_forecasts = []
        for row in detailed_rows:
            forecast_text_div = row.find('div', class_='forecast-text')
            if forecast_text_div:
                detailed_forecasts.append(forecast_text_div.get_text(strip=True))
            else:
                detailed_forecasts.append('')

        # Apply precipitation and wind rules
        def process_tile_with_detailed(tile, detailed_text):
            """Apply precipitation % and wind rules from detailed forecast"""
            condition = tile['condition']
            temp = tile['temp']

            # Precipitation rule: Replace vague wording with explicit %
            precip_keywords = ['Chance', 'Slight', 'Likely', 'Showers', 'T-storms', 'Rain']
            has_precip_mention = any(keyword.lower() in condition.lower() for keyword in precip_keywords)

            if has_precip_mention and detailed_text:
                # Look for explicit percentage in detailed forecast
                precip_match = re.search(r'(\d+)\s*percent', detailed_text, re.IGNORECASE)
                if precip_match:
                    percent = precip_match.group(1)
                    condition = f"{percent}% chance of precipitation"

            # Wind rule: Only include if gusts > 25 mph
            wind_info = ''
            if detailed_text:
                gust_match = re.search(r'gusts?\s+as\s+high\s+as\s+(\d+)\s*mph', detailed_text, re.IGNORECASE)
                if gust_match:
                    gust_speed = int(gust_match.group(1))
                    if gust_speed > 25:
                        wind_info = f" with gusts up to {gust_speed} mph"

            return condition, temp, wind_info

        # Process each tile
        today_condition, today_temp, today_wind = process_tile_with_detailed(tiles[0], detailed_forecasts[0])
        tonight_condition, tonight_temp, tonight_wind = process_tile_with_detailed(tiles[1], detailed_forecasts[1])
        tomorrow_condition, tomorrow_temp, tomorrow_wind = process_tile_with_detailed(tiles[2], detailed_forecasts[2])

        # Extract temperature values
        def extract_temp(temp_str):
            """Extract numeric temperature from string like 'High: 82 °F'"""
            match = re.search(r'(\d+)', temp_str)
            return match.group(1) if match else temp_str

        today_high = extract_temp(today_temp)
        tonight_low = extract_temp(tonight_temp)
        tomorrow_high = extract_temp(tomorrow_temp)

        # Get current date
        current_date = datetime.now().strftime('%-m/%-d/%Y')

        # Build formatted weather string
        formatted_parts = []
        formatted_parts.append(f"Today {current_date}: {today_condition} with a high of {today_high}°F dropping to {tonight_low}°F overnight")

        # Add wind/precip modifiers for today if present
        if today_wind:
            formatted_parts.append(today_wind.strip())

        formatted_parts.append(f". Tonight: {tonight_condition}")

        # Add wind for tonight if present
        if tonight_wind:
            formatted_parts.append(tonight_wind.strip())

        formatted_parts.append(f". Tomorrow: {tomorrow_condition} with a high of {tomorrow_high}°F")

        # Add wind for tomorrow if present
        if tomorrow_wind:
            formatted_parts.append(tomorrow_wind.strip())

        formatted_parts.append(".")

        formatted_weather = ''.join(formatted_parts)

        # Return data
        return jsonify({
            'error': False,
            'date': current_date,
            'tiles': {
                'today': {'condition': today_condition, 'temp': today_high, 'wind': today_wind},
                'tonight': {'condition': tonight_condition, 'temp': tonight_low, 'wind': tonight_wind},
                'tomorrow': {'condition': tomorrow_condition, 'temp': tomorrow_high, 'wind': tomorrow_wind}
            },
            'detailed_forecasts': detailed_forecasts,
            'formatted_weather': formatted_weather
        })

    except Exception as e:
        print(f"Weather API error: {str(e)}")
        return jsonify({
            'error': True,
            'formatted_weather': 'Weather unavailable - please add manually'
        })


if __name__ == '__main__':
    # Run the Flask development server
    # Access at http://localhost:3000
    app.run(host='0.0.0.0', port=3000, debug=True)