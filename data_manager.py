"""
Data Manager - JSON Operations
Handles reading and writing JSON files for the garden dashboard
"""

import json
from pathlib import Path
from typing import Dict, List, Optional


class DataManager:
    """
    Manages all JSON data operations for the garden dashboard

    Handles:
    - Reading plant data from individual JSON files (including inactive subdirectory)
    - Reading shared data (containers, products, meta)
    - Reading dashboard order configuration
    - Writing updates to JSON files
    - Validating data structure
    """

    def __init__(self, data_dir: Path):
        """
        Initialize the DataManager

        Args:
            data_dir: Path to the data directory containing JSON files
        """
        self.data_dir = Path(data_dir)
        self.plants_dir = self.data_dir / 'plants'
        self.containers_file = self.data_dir / 'containers.json'
        self.products_file = self.data_dir / 'products.json'
        self.meta_file = self.data_dir / 'meta.json'
        self.dashboard_order_file = self.data_dir / 'dashboard_order.json'

    def get_all_plants(self) -> List[Dict]:
        """
        Load all plant JSON files from plants directory and plants/inactive subdirectory

        Scans both locations to support dynamic file organization without code changes.
        Plants can be moved between active and inactive directories freely.

        Returns:
            List of plant dictionaries, sorted by plant name
        """
        plants = []

        if not self.plants_dir.exists():
            print(f"Warning: Plants directory not found: {self.plants_dir}")
            return plants

        # Read all JSON files in the main plants directory
        for plant_file in self.plants_dir.glob('*.json'):
            try:
                with open(plant_file, 'r', encoding='utf-8') as f:
                    plant_data = json.load(f)
                    plants.append(plant_data)
            except json.JSONDecodeError as e:
                print(f"Error parsing {plant_file.name}: {e}")
            except Exception as e:
                print(f"Error reading {plant_file.name}: {e}")

        # Also read from plants/inactive subdirectory if it exists
        inactive_dir = self.plants_dir / 'inactive'
        if inactive_dir.exists() and inactive_dir.is_dir():
            for plant_file in inactive_dir.glob('*.json'):
                try:
                    with open(plant_file, 'r', encoding='utf-8') as f:
                        plant_data = json.load(f)
                        plants.append(plant_data)
                except json.JSONDecodeError as e:
                    print(f"Error parsing {plant_file.name}: {e}")
                except Exception as e:
                    print(f"Error reading {plant_file.name}: {e}")

        # Sort by plant name
        plants.sort(key=lambda x: x.get('plant', ''))
        return plants

    def get_dashboard_order(self) -> List[Dict]:
        """
        Load dashboard order configuration

        Returns:
            List of category dictionaries with plant IDs
        """
        if not self.dashboard_order_file.exists():
            print(f"Warning: Dashboard order file not found: {self.dashboard_order_file}")
            return []

        try:
            with open(self.dashboard_order_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('categories', [])
        except json.JSONDecodeError as e:
            print(f"Error parsing dashboard_order.json: {e}")
            return []
        except Exception as e:
            print(f"Error reading dashboard_order.json: {e}")
            return []

    def get_ordered_plants(self) -> List[Dict]:
        """
        Get plants organized by dashboard order

        Returns:
            List of category dictionaries containing plant data
        """
        # Load all plants into a lookup dictionary
        all_plants_list = self.get_all_plants()
        all_plants = {plant['id']: plant for plant in all_plants_list if 'id' in plant}

        # Load dashboard order
        categories = self.get_dashboard_order()

        # Build ordered list with actual plant data
        ordered_categories = []
        for category in categories:
            category_data = category.copy()
            category_data['plants'] = []

            # Look up each plant ID
            for plant_id in category.get('plants', []):
                if plant_id in all_plants:
                    category_data['plants'].append(all_plants[plant_id])
                else:
                    print(f"Warning: Plant {plant_id} not found in plants directory")

            ordered_categories.append(category_data)

        return ordered_categories

    def get_plant(self, plant_id: str) -> Optional[Dict]:
        """
        Load a specific plant by ID

        Searches both plants/ and plants/inactive/ directories

        Args:
            plant_id: The plant's unique identifier (e.g., 'basil_001')

        Returns:
            Plant dictionary if found, None otherwise
        """
        # Check main plants directory first
        plant_file = self.plants_dir / f'{plant_id}.json'

        if plant_file.exists():
            try:
                with open(plant_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError as e:
                print(f"Error parsing {plant_file.name}: {e}")
                return None
            except Exception as e:
                print(f"Error reading {plant_file.name}: {e}")
                return None

        # Check inactive subdirectory
        inactive_file = self.plants_dir / 'inactive' / f'{plant_id}.json'

        if inactive_file.exists():
            try:
                with open(inactive_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError as e:
                print(f"Error parsing {inactive_file.name}: {e}")
                return None
            except Exception as e:
                print(f"Error reading {inactive_file.name}: {e}")
                return None

        print(f"Warning: Plant file not found: {plant_id}.json")
        return None

    def save_plant(self, plant_id: str, plant_data: Dict) -> bool:
        """
        Save plant data to a JSON file

        Saves to plants/ directory by default.
        To save to inactive/, manually specify the file path or move the file after saving.

        Args:
            plant_id: The plant's unique identifier
            plant_data: Complete plant dictionary to save

        Returns:
            True if successful, False otherwise
        """
        plant_file = self.plants_dir / f'{plant_id}.json'

        try:
            # Ensure plants directory exists
            self.plants_dir.mkdir(parents=True, exist_ok=True)

            # Write with nice formatting
            with open(plant_file, 'w', encoding='utf-8') as f:
                json.dump(plant_data, f, indent=2, ensure_ascii=False)

            return True
        except Exception as e:
            print(f"Error saving {plant_file.name}: {e}")
            return False

    def get_containers(self) -> List[Dict]:
        """
        Load all containers from containers.json

        Returns:
            List of container dictionaries
        """
        if not self.containers_file.exists():
            print(f"Warning: Containers file not found: {self.containers_file}")
            return []

        try:
            with open(self.containers_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            print(f"Error parsing containers.json: {e}")
            return []
        except Exception as e:
            print(f"Error reading containers.json: {e}")
            return []

    def get_products(self) -> List[Dict]:
        """
        Load all products from products.json

        Returns:
            List of product dictionaries
        """
        if not self.products_file.exists():
            print(f"Warning: Products file not found: {self.products_file}")
            return []

        try:
            with open(self.products_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            print(f"Error parsing products.json: {e}")
            return []
        except Exception as e:
            print(f"Error reading products.json: {e}")
            return []

    def get_metadata(self) -> Dict:
        """
        Load metadata from meta.json

        Returns:
            Metadata dictionary
        """
        if not self.meta_file.exists():
            print(f"Warning: Meta file not found: {self.meta_file}")
            return {}

        try:
            with open(self.meta_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('metadata', {})
        except json.JSONDecodeError as e:
            print(f"Error parsing meta.json: {e}")
            return {}
        except Exception as e:
            print(f"Error reading meta.json: {e}")
            return {}

    def save_containers(self, containers: List[Dict]) -> bool:
        """
        Save containers to containers.json

        Args:
            containers: List of container dictionaries

        Returns:
            True if successful, False otherwise
        """
        try:
            with open(self.containers_file, 'w', encoding='utf-8') as f:
                json.dump(containers, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving containers.json: {e}")
            return False

    def save_products(self, products: List[Dict]) -> bool:
        """
        Save products to products.json

        Args:
            products: List of product dictionaries

        Returns:
            True if successful, False otherwise
        """
        try:
            with open(self.products_file, 'w', encoding='utf-8') as f:
                json.dump(products, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving products.json: {e}")
            return False

    def get_active_plants(self) -> List[Dict]:
        """
        Get only active plants (status = 'Active')

        Returns:
            List of active plant dictionaries
        """
        all_plants = self.get_all_plants()
        return [p for p in all_plants if p.get('status') == 'Active']

    def get_inactive_plants(self) -> List[Dict]:
        """
        Get only inactive plants (status = 'Inactive')

        Returns:
            List of inactive plant dictionaries
        """
        all_plants = self.get_all_plants()
        return [p for p in all_plants if p.get('status') == 'Inactive']