"""
Master Garden Dashboard - Flask Application
Simple, self-hosted web application for garden management
"""

from flask import Flask, render_template, jsonify, request, flash, redirect, url_for
import os
import json
from pathlib import Path
from datetime import datetime, timedelta
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
            output_lines.append('```json')
            output_lines.append(plant_json)
            output_lines.append('```')
            output_lines.append('')
            output_lines.append(after_json_content)

            output_message = '\n'.join(output_lines)
            output_title = "Start Channel"

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

        # Remove markdown code fences if present
        json_input = re.sub(r'^```json\s*\n', '', json_input, flags=re.MULTILINE)
        json_input = re.sub(r'\n```\s*$', '', json_input, flags=re.MULTILINE)
        json_input = json_input.strip()

        # Handle trailing commas (common JSON error from GPT)
        json_input = re.sub(r',(\s*[}\]])', r'\1', json_input)

        # Parse JSON
        try:
            parsed_data = json.loads(json_input)
        except json.JSONDecodeError as e:
            return render_template(
                'journal_update.html',
                plants=data_manager.get_all_plants(),
                error=True,
                error_message="Invalid JSON format",
                error_details=str(e)
            )

        # Load plant
        plant = data_manager.get_plant(plant_id)
        if not plant:
            return render_template(
                'journal_update.html',
                plants=data_manager.get_all_plants(),
                error=True,
                error_message=f"Plant not found: {plant_id}"
            )

        # Determine action type and field
        action_type = ""

        if action == 'journal':
            # Validate journal entry has required fields
            required_fields = ['date', 'time', 'conditions', 'digital_probe', 'observations']
            missing_fields = [f for f in required_fields if f not in parsed_data]

            if missing_fields:
                return render_template(
                    'journal_update.html',
                    plants=data_manager.get_all_plants(),
                    error=True,
                    error_message=f"Missing required fields: {', '.join(missing_fields)}"
                )

            # Add new journal entry
            if 'journal' not in plant:
                plant['journal'] = []

            plant['journal'].insert(0, parsed_data)  # Insert at beginning (newest first)
            action_type = "Journal Entry Added"

        elif action == 'plant_main':
            # Update plant main data fields
            # Only update fields that exist in the parsed data
            updatable_fields = ['whats_been_logged', 'current_stage', 'current_state', 'timeline']

            updated_fields = []
            for field in updatable_fields:
                if field in parsed_data:
                    plant[field] = parsed_data[field]
                    updated_fields.append(field)

            if not updated_fields:
                return render_template(
                    'journal_update.html',
                    plants=data_manager.get_all_plants(),
                    error=True,
                    error_message="No valid plant main data fields found to update"
                )

            action_type = f"Plant Main Data Updated ({', '.join(updated_fields)})"

        # Save updated plant
        data_manager.save_plant(plant_id, plant)

        # Return success
        return render_template(
            'journal_update.html',
            plants=[],
            success=True,
            plant_name=plant.get('plant', plant_id),
            entry_date=parsed_data.get('date', 'N/A') if action == 'journal' else 'N/A',
            entry_time=parsed_data.get('time', 'N/A') if action == 'journal' else 'N/A',
            action_type=action_type,
            total_entries=len(plant['journal']),
        )

    except Exception as e:
        return render_template(
            'journal_update.html',
            plants=data_manager.get_all_plants(),
            error=True,
            error_message="Unexpected error occurred",
            error_details=str(e)
        )


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

        # Use provided ID if present, otherwise generate new one
        if 'id' in new_data and new_data['id']:
            new_id = new_data['id']
        else:
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
        time_override = request.form.get('time_override', '').strip()
        include_questions = request.form.get('include_questions')
        files = request.files.getlist('photos')

        # Validation - re-render form with existing data on error
        all_plants = data_manager.get_all_plants()
        available_plant_ids = sorted([p.get('id') for p in all_plants if p.get('id') and p.get('status') != 'Inactive'])

        if not plant_id:
            return render_template(
                'photo_prep.html',
                current_date=date_str if date_str else datetime.now().strftime('%Y-%m-%d'),
                available_plants=available_plant_ids,
                error=True,
                error_message='Plant ID is required',
                plant_id='',
                context=context,
                starting_number=starting_number,
                global_message=global_message,
                plant_message=plant_message,
                time_override=time_override
            )

        # Verify plant exists
        plant = data_manager.get_plant(plant_id)
        if not plant:
            return render_template(
                'photo_prep.html',
                current_date=date_str if date_str else datetime.now().strftime('%Y-%m-%d'),
                available_plants=available_plant_ids,
                error=True,
                error_message=f'Plant not found: {plant_id}. Please check the Plant ID and try again.',
                plant_id=plant_id,
                context=context,
                starting_number=starting_number,
                global_message=global_message,
                plant_message=plant_message,
                time_override=time_override
            )

        if context == 'Initial' and (not files or files[0].filename == ''):
            return render_template(
                'photo_prep.html',
                current_date=date_str if date_str else datetime.now().strftime('%Y-%m-%d'),
                available_plants=available_plant_ids,
                error=True,
                error_message='At least one photo is required for Initial context',
                plant_id=plant_id,
                context=context,
                starting_number=starting_number,
                global_message=global_message,
                plant_message=plant_message,
                time_override=time_override
            )

        if not date_str:
            return render_template(
                'photo_prep.html',
                current_date=datetime.now().strftime('%Y-%m-%d'),
                available_plants=available_plant_ids,
                error=True,
                error_message='Date is required',
                plant_id=plant_id,
                context=context,
                starting_number=starting_number,
                global_message=global_message,
                plant_message=plant_message,
                time_override=time_override
            )

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
                    file.save(str(temp_path))

                    # Open and process image
                    try:
                        with Image.open(temp_path) as img:
                            # Auto-rotate based on EXIF orientation
                            from PIL import ImageOps
                            img = ImageOps.exif_transpose(img)

                            # Convert to RGB if needed
                            if img.mode in ('RGBA', 'P', 'LA'):
                                rgb_img = Image.new('RGB', img.size, (255, 255, 255))
                                if img.mode == 'P':
                                    img = img.convert('RGBA')
                                rgb_img.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
                                img = rgb_img
                            elif img.mode != 'RGB':
                                img = img.convert('RGB')

                            # Compress and save
                            img.save(str(file_path), 'JPEG', quality=COMPRESSION_QUALITY, optimize=True)

                        # Clean up temp file
                        temp_path.unlink()

                        # Add to processed files (always include, probe indicator added later)
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

                except Exception as e:
                    print(f"Error with file {file.filename}: {str(e)}")
                    raise

        # Generate output message
        output_lines = []
        import pytz
        eastern = pytz.timezone('US/Eastern')

        # Determine time to use (override or current)
        if time_override:
            display_time = time_override
        else:
            display_time = datetime.now(eastern).strftime('%-I:%M %p')

        # Save original global message for form reload
        original_global_message = global_message

        if context == 'Follow-Up':
            # FOLLOW-UP TEMPLATE (NEW FORMAT)
            output_lines.append(f'{display_time} Same Day Follow-up')
            output_lines.append('')
            output_lines.append(plant_message if plant_message else '[your follow-up text here]')
            output_lines.append('')
            output_lines.append('First, make sure you have today\'s most recent Daily Journal Entry JSON in context because I will have you update it after we discuss and I don\'t want you reconstructing or inventing a replacement JSON.')
            output_lines.append('')
            output_lines.append('Then, respond naturally. Then re-issue today\'s most recent COMPLETE Daily Journal Entry JSON (above in this chat) and change nothing other than the following:')

            # Conditionally add photos section
            if processed_files:
                output_lines.append('')
                output_lines.append('New photo(s) to append to existing `photos` array (generate a real caption + tags for each — no blanks):')
                for idx, filename in enumerate(processed_files, 1):
                    # Check if this photo was marked as a probe reading
                    probe_checkbox_name = f"probe_reading_{idx - 1}"  # 0-indexed in form
                    is_probe = request.form.get(probe_checkbox_name) == 'on'

                    if is_probe:
                        output_lines.append(f'{idx}. {filename}  ← (probe reading)')
                    else:
                        output_lines.append(f'{idx}. {filename}')

            # Always add follow-up section
            output_lines.append('')
            output_lines.append('New follow-up to append to existing `follow_up` array:')
            output_lines.append(f'"[{display_time}] {{replace with narrative summary}}"')

            # Conditionally add q_and_a_summary section
            if include_questions:
                output_lines.append('')
                output_lines.append('Update `q_and_a_summary` by APPENDING a short narrative summary of the new question(s) + answer(s) to the existing text (do not overwrite).')

            # Add photo reminder only if photos were uploaded
            if processed_files:
                output_lines.append('')
                output_lines.append('If photo filenames are listed but no photos were uploaded, reply only: "Please provide the photos referenced." and wait for them before responding further.')

            # COMMENTED OUT - Keep for reference if needed
            # output_lines.append('')
            # output_lines.append('Output valid JSON only (exact schema, no invented fields).')
            # output_lines.append('Do NOT change the Daily Journal Entry `time` (it remains the probe timestamp).')
            # output_lines.append('Do NOT reconstruct or invent a replacement JSON.')

        else:
            # INITIAL TEMPLATE (EXISTING)
            # Replace variables in global message
            if global_message:
                global_message = global_message.replace('{id}', plant_id)
                global_message = global_message.replace('{plant}', plant.get('plant', plant_id))
                global_message = global_message.replace('{garden_location}', plant.get('garden_location', ''))
                global_message = global_message.replace('{full_sun_start}', plant.get('full_sun_start', ''))
                output_lines.append(global_message)
                output_lines.append('')

            if plant_message:
                plant_message = plant_message.replace('{id}', plant_id)
                plant_message = plant_message.replace('{plant}', plant.get('plant', plant_id))
                plant_message = plant_message.replace('{garden_location}', plant.get('garden_location', ''))
                plant_message = plant_message.replace('{full_sun_start}', plant.get('full_sun_start', ''))
                output_lines.append(plant_message)
                output_lines.append('')

            if processed_files:
                output_lines.append('Here are the photo names:')
                for idx, filename in enumerate(processed_files, 1):
                    # Check if this photo was marked as a probe reading
                    probe_checkbox_name = f"probe_reading_{idx - 1}"  # 0-indexed in form
                    is_probe = request.form.get(probe_checkbox_name) == 'on'

                    if is_probe:
                        output_lines.append(f'{idx}. {filename}  ← (probe reading)')
                    else:
                        output_lines.append(f'{idx}. {filename}')

            # Add watering assessment prompt if checkbox is checked
            include_watering = request.form.get('include_watering')
            if include_watering:
                # Parse the date from the form
                form_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                today = datetime.now(eastern).date()

                # Check if form date is today or yesterday
                if form_date == today:
                    # Same day - ask about watering tomorrow morning
                    output_lines.append('')
                    output_lines.append(f'It is now {display_time}. Should I water at 6:00 AM tomorrow morning?')
                elif form_date == today - timedelta(days=1):
                    # Form date is yesterday - ask about watering right now
                    output_lines.append('')
                    output_lines.append(f'It is now {display_time} the following day. Should I water right now?')
                else:
                    # Form date is neither today nor yesterday - generic prompt
                    output_lines.append('')
                    output_lines.append(f'It is now {display_time}. Should I water?')

                output_lines.append('')

            # Always include these instructions for Initial context
            output_lines.append('')
            output_lines.append('Please provide:')
            output_lines.append('Full Expert Assessment → Daily Journal Entry JSON → Plant Main Data Review (silently) → Result')
            output_lines.append('')
            output_lines.append('If any required inputs are missing, ask me for them before beginning.')
            output_lines.append('')

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
            plant_message=plant_message if 'plant_message' in locals() else '',
            time_override=time_override if 'time_override' in locals() else ''
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

        # Parse date
        date_obj = datetime.strptime(date_str, '%m/%d/%Y')
        date_filename = date_obj.strftime('%Y%m%d')

        # Generate filename
        filename = f"{plant_id}-{date_filename}-{photo_index.zfill(2)}.jpeg"

        # Create plant subfolder
        plant_folder = PHOTO_BASE_PATH / plant_id
        plant_folder.mkdir(parents=True, exist_ok=True)
        file_path = plant_folder / filename

        # Save temp file
        temp_path = plant_folder / f"temp_placeholder_{filename}"
        file.save(str(temp_path))

        # Process image
        try:
            with Image.open(temp_path) as img:
                # Auto-rotate based on EXIF
                from PIL import ImageOps
                img = ImageOps.exif_transpose(img)

                # Convert to RGB
                if img.mode in ('RGBA', 'P', 'LA'):
                    rgb_img = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'P':
                        img = img.convert('RGBA')
                    rgb_img.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
                    img = rgb_img
                elif img.mode != 'RGB':
                    img = img.convert('RGB')

                # Save compressed
                img.save(str(file_path), 'JPEG', quality=COMPRESSION_QUALITY, optimize=True)

            temp_path.unlink()

        except Exception as img_error:
            if temp_path.exists():
                temp_path.unlink()
            raise

        # Update plant JSON
        plant = data_manager.get_plant(plant_id)
        if plant and 'journal' in plant:
            # Find matching journal entry
            for entry in plant['journal']:
                entry_date = entry.get('date', '')
                if entry_date == date_str:
                    # Update photos array
                    if 'photos' not in entry:
                        entry['photos'] = []

                    # Find or add photo entry
                    photo_updated = False
                    for photo in entry['photos']:
                        if photo.get('file_name') == filename:
                            photo_updated = True
                            break

                    if not photo_updated:
                        entry['photos'].append({
                            'file_name': filename,
                            'caption': 'Placeholder caption - update as needed',
                            'tags': 'placeholder'
                        })

                    # Save updated plant
                    data_manager.save_plant(plant_id, plant)
                    break

        return jsonify({
            'success': True,
            'photo_url': f'/photos/{plant_id}/{filename}'
        })

    except Exception as e:
        print(f"Error uploading placeholder photo: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/photos/<plant_id>/<filename>')
def serve_photo(plant_id, filename):
    """Serve photos from Google Drive folder"""
    try:
        photo_path = PHOTO_BASE_PATH / plant_id / filename
        if photo_path.exists():
            from flask import send_file
            return send_file(str(photo_path))
        else:
            return "Photo not found", 404
    except Exception as e:
        return f"Error serving photo: {str(e)}", 500


@app.route('/api/plant/<plant_id>/last-photo-number', methods=['GET'])
def get_last_photo_number(plant_id):
    """
    Get the last photo number for a plant on a specific date
    Used for Follow-Up context to auto-populate starting photo number
    """
    try:
        date_param = request.args.get('date', '')
        if not date_param:
            return jsonify({'error': 'Date parameter required'}), 400

        # Parse date from YYYY-MM-DD format
        date_obj = datetime.strptime(date_param, '%Y-%m-%d')
        journal_date = date_obj.strftime('%-m/%-d/%Y')  # Convert to M/D/YYYY for matching

        # Load plant
        plant = data_manager.get_plant(plant_id)
        if not plant:
            return jsonify({'error': f'Plant not found: {plant_id}'}), 404

        if 'journal' not in plant or len(plant['journal']) == 0:
            return jsonify({'error': 'No journal entries found for this plant'}), 404

        # Find journal entry for this date
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

            # Replace line breaks with spaces (NWS uses <br> tags)
            condition_text = short_desc.get_text(separator=' ', strip=True) if short_desc else ''
            condition_text = ' '.join(condition_text.split())  # Normalize multiple spaces

            tiles.append({
                'period': period_name.get_text(strip=True) if period_name else '',
                'condition': condition_text,
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

        # Process each tile and normalize whitespace
        today_condition, today_temp, today_wind = process_tile_with_detailed(tiles[0], detailed_forecasts[0])
        today_condition = ' '.join(today_condition.split())  # Normalize whitespace

        tonight_condition, tonight_temp, tonight_wind = process_tile_with_detailed(tiles[1], detailed_forecasts[1])
        tonight_condition = ' '.join(tonight_condition.split())  # Normalize whitespace

        tomorrow_condition, tomorrow_temp, tomorrow_wind = process_tile_with_detailed(tiles[2], detailed_forecasts[2])
        tomorrow_condition = ' '.join(tomorrow_condition.split())  # Normalize whitespace

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