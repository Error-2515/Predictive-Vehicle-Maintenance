from tinydb import TinyDB, Query
from datetime import datetime
from tinydb.storages import JSONStorage
import json

# Fixed PrettyJSONStorage with self._filename
class PrettyJSONStorage(JSONStorage):
    def __init__(self, path, **kwargs):
        super().__init__(path, **kwargs)
        self._filename = path

    def write(self, data):
        with open(self._filename, 'w') as f:
            json.dump(data, f, indent=4)

# Initialize TinyDB
db = TinyDB('vehicle_parts_db.json', storage=PrettyJSONStorage)

# Register a new vehicle
def register_vehicle_in_tinydb(vehicle_info):
    Vehicle = Query()
    if db.search(Vehicle.number_plate == vehicle_info['number_plate']):
        return {'status': 'exists', 'message': f"Vehicle {vehicle_info['number_plate']} already exists in TinyDB."}

    db.insert({
        'number_plate': vehicle_info['number_plate'],
        'owner_name': vehicle_info['owner_name'],
        'vehicle_type': vehicle_info['vehicle_type'],
        'make_year': vehicle_info['make_year'],
        'color': vehicle_info['color'],
        'phone_number': vehicle_info['phone_number'],
        'fuel_type': vehicle_info['fuel_type'],
        'transmission_type': vehicle_info['transmission_type'],
        'engine_size': vehicle_info['engine_size'],
        'odometer_reading': vehicle_info['odometer_reading'],
        'fuel_efficiency': vehicle_info['fuel_efficiency'],
        'tire_condition': vehicle_info['tire_condition'],
        'brake_condition': vehicle_info['brake_condition'],
        'battery_status': vehicle_info['battery_status'],
        'owner_type': vehicle_info['battery_status'],
        'accident_history': vehicle_info['accident_history'],
        'parts': []
    })

    return {'status': 'success', 'message': f"Vehicle {vehicle_info['number_plate']} registered in TinyDB."}

# Add part to existing vehicle
def add_part_to_vehicle(number_plate, part_info):
    Vehicle = Query()
    vehicle = db.search(Vehicle.number_plate == number_plate)

    if not vehicle:
        return {'status': 'not_found', 'message': f"Vehicle {number_plate} not found in TinyDB."}

    db.update({'parts': vehicle[0]['parts'] + [part_info]}, Vehicle.number_plate == number_plate)

    return {'status': 'success', 'message': f"Part added to vehicle {number_plate}."}

# Fetch vehicle and part info
def fetch_vehicle_with_parts(number_plate):
    Vehicle = Query()
    vehicle = db.search(Vehicle.number_plate == number_plate)

    if not vehicle:
        return {'status': 'not_found', 'message': f"Vehicle {number_plate} not found."}

    vehicle_data = vehicle[0]
    today = datetime.now().date()

    enriched_parts = []
    for part in vehicle_data['parts']:
        try:
            last_service = datetime.strptime(part['last_service_date'], "%Y-%m-%d").date()
            days_since_service = (today - last_service).days
        except Exception:
            days_since_service = None

        enriched_parts.append({
            **part,
            'days_since_service': days_since_service
        })

    return {
        'status': 'success',
        'message': f"Fetched vehicle {number_plate} successfully.",
        'vehicle_info': vehicle_data,
        'parts': enriched_parts
    }

# Console input helpers (optional usage)
def input_vehicle_details():
    number_plate = input("Enter Vehicle Number Plate: ")
    owner_name = input("Enter Owner Name: ")
    model = input("Enter Vehicle Model: ")
    make_year = int(input("Enter Make Year: "))
    color = input("Enter Vehicle Color: ")
    phone_number = input("Enter Owner's Phone Number: ")

    return {
        'number_plate': number_plate,
        'owner_name': owner_name,
        'model': model,
        'make_year': make_year,
        'color': color,
        'phone_number': phone_number
    }

def input_part_details():
    vehicle_part = input("Enter Part Name: ")
    manufacture_date = input("Enter Manufacture Date (YYYY-MM-DD): ")
    last_service_date = input("Enter Last Service Date (YYYY-MM-DD): ")
    condition_notes = input("Enter Condition Notes: ")

    return {
        'vehicle_part': vehicle_part,
        'manufacture_date': manufacture_date,
        'last_service_date': last_service_date,
        'condition_notes': condition_notes
    }


# Update a specific part for a vehicle
def update_part_for_vehicle(number_plate, vehicle_part, updated_part):
    Vehicle = Query()
    vehicles = db.search(Vehicle.number_plate == number_plate)
    if not vehicles:
        return False

    parts = vehicles[0]["parts"]
    for idx, part in enumerate(parts):
        if part["vehicle_part"] == vehicle_part:
            parts[idx] = updated_part
            break

    db.update({'parts': parts}, Vehicle.number_plate == number_plate)
    return True

# Update vehicle's last serviced field
def update_vehicle_last_serviced(number_plate, mechanic_note=""):
    Vehicle = Query()
    vehicle = db.search(Vehicle.number_plate == number_plate)
    if not vehicle:
        return False

    update_fields = {'last_serviced': datetime.now().strftime("%Y-%m-%d")}
    if mechanic_note.strip():
        update_fields['mechanic_note'] = mechanic_note.strip()

    db.update(update_fields, Vehicle.number_plate == number_plate)
    return True

def update_vehicle_odometer(number_plate, new_km):
    Vehicle = Query()
    results = db.search(Vehicle.number_plate == number_plate)
    if results:
        vehicle = results[0]
        vehicle["Odometer_Reading"] = new_km
        db.update(vehicle, Vehicle.number_plate == number_plate)


# Example CLI usage (optional testing)
if __name__ == "__main__":
    print("Register Vehicle")
    vehicle_info = input_vehicle_details()
    print(register_vehicle_in_tinydb(vehicle_info))

    print("Add Part to Vehicle")
    part_info = input_part_details()
    number_plate = vehicle_info['number_plate']
    print(add_part_to_vehicle(number_plate, part_info))

    print("Fetching Vehicle and Parts Details")
    result = fetch_vehicle_with_parts(number_plate)
    print(result)
