from tinydb import TinyDB, Query
import joblib
import pandas as pd

# Load the model and encoders
model = joblib.load("vehicle_rul_model.pkl")
vehicle_type_encoder = joblib.load("vehicle_type_encoder.pkl")
part_name_encoder = joblib.load("vehicle_part_encoder.pkl")

# Load the TinyDB
db = TinyDB("vehicle_parts_db.json")

def predict_rul_from_db(number_plate: str):
    Vehicle = Query()
    results = db.search(Vehicle.number_plate == number_plate)

    if not results:
        print(f"❌ No record found for number plate: {number_plate}")
        return

    vehicle = results[0]
    vehicle_type = vehicle.get("vehicle_type", "unknown")
    total_km_raw = vehicle.get("total_km", "0")

    try:
        total_km = float(total_km_raw)
    except ValueError:
        print(f"⚠️ Invalid total_km value: {total_km_raw}. Defaulting to 0.")
        total_km = 0.0

    print(f"\n🔍 Found vehicle: {vehicle_type.upper()} - {number_plate}")

    for part in vehicle.get("parts", []):
        part_name = part.get("vehicle_part", "unknown")
        last_service_km_raw = part.get("last_service_km", "0")

        try:
            last_service_km = float(last_service_km_raw)
        except ValueError:
            print(f"⚠️ Invalid last_service_km for part '{part_name}'. Skipping.")
            continue

        # Encode categorical features
        try:
            vehicle_type_encoded = vehicle_type_encoder.transform([vehicle_type.lower()])[0]
            part_name_encoded = part_name_encoder.transform([part_name.lower()])[0]
        except ValueError:
            print(f"⚠️ Unknown category (vehicle_type: '{vehicle_type}', part: '{part_name}')")
            continue

        # Prepare input for prediction
        input_df = pd.DataFrame([{
            'vehicle_type': vehicle_type_encoded,
            'vehicle_part': part_name_encoded,
            'total_km': total_km,
            'last_service_km': last_service_km
        }])

        try:
            predicted_rul = model.predict(input_df)[0]
            print(f"🔧 Part: {part_name} → Predicted RUL: {predicted_rul:.0f} km")

            # Update RUL in database
            part["RUL_km"] = predicted_rul

        except Exception as e:
            print(f"⚠️ Could not predict RUL for part '{part_name}': {e}")

    # Save updates to database
    db.update(vehicle, Vehicle.number_plate == number_plate)


# 🔘 MAIN INTERACTIVE SECTION
if __name__ == "__main__":
    print("🚗 Vehicle Part RUL Predictor")
    
    number_plate_input = 'TS15AB1239'

    if number_plate_input.lower() == 'exit':
        print("👋 Exiting. Have a great day!")
        

    predict_rul_from_db(number_plate_input)
