from tinydb import TinyDB, Query
import joblib
import pandas as pd

# Load the model
model = joblib.load("vehicle_rul_model.pkl")

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

        # Prepare input for prediction
        input_df = pd.DataFrame([{
            'vehicle_type': str(vehicle_type),
            'vehicle_part': part_name,
            'total_km': total_km,
            'last_service_km': last_service_km
        }])

        try:
            predicted_rul = round(model.predict(input_df)[0])
            print(f"🔧 Part: {part_name} → Predicted RUL: {predicted_rul} km")

            # Update RUL in database
            part["RUL_km"] = predicted_rul

        except Exception as e:
            print(f"⚠️ Could not predict RUL for part '{part_name}': {e}")

    # Save updates to database
    db.update(vehicle, Vehicle.number_plate == number_plate)


# 🔘 MAIN INTERACTIVE SECTION
if __name__ == "__main__":
    print("🚗 Vehicle Part RUL Predictor")
    while True:
        number_plate_input = input("Enter vehicle number plate (or type 'exit' to quit): ").strip()

        if number_plate_input.lower() == 'exit':
            print("👋 Exiting. Have a great day!")
            break

        predict_rul_from_db(number_plate_input)
