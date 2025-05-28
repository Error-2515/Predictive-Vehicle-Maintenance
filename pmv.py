from tinydb import TinyDB, Query
import pandas as pd
import joblib

# Load the trained model
model = joblib.load('maintenance_model.pkl')


def predict_by_number_plate(number_plate, db_path='vehicle_parts_db.json'):
    # Load database
    db = TinyDB(db_path)
    Vehicle = Query()
    
    # Search by number plate (standardized to uppercase with no extra spaces)
    record = db.get(Vehicle.number_plate == number_plate.upper().strip())

    if not record:
        print(f"❌ Vehicle with number plate '{number_plate}' not found in database.")
        return

    # Extract and prepare input data
    user_input = {
        'Mileage': record.get('Odometer_Reading', 0),  # you can calculate actual mileage if available
        'Vehicle_Age': pd.Timestamp.now().year - int(record.get('make_year', 2020)),
        'Engine_Size': float(record.get('Engine_Size', 0)),
        'Odometer_Reading': float(record.get('Odometer_Reading', 0)),
        'Days_Since_Service': int(record.get('Days_Since_Service', 180)),  # estimate if not stored
        'Days_Until_Warranty_Expires': int(record.get('Days_Until_Warranty_Expires', 300)),
        'Owner_Type': int(record.get('Owner_Type', 1)),
        'Service_History': int(record.get('Service_History', 3)),
        'Accident_History': int(record.get('Accident_History', 0)),
        'Fuel_Efficiency': float(record.get('Fuel_Efficiency', 12.0)),

        'Fuel_Type': record.get('Fuel_Type', 'Petrol').title(),
        'Maintenance_History': record.get('Maintenance_History', 'Good').title(),
        'Transmission_Type': record.get('Transmission_Type', 'Manual').title(),
        'Tire_Condition': record.get('Tire_Condition', 'Good').title(),
        'Brake_Condition': record.get('Brake_Condition', 'Good').title(),
        'Battery_Status': record.get('Battery_Status', 'Good').title()
    }

    # Feature names expected by the model
    feature_columns = [
        'Mileage', 'Vehicle_Age', 'Engine_Size', 'Odometer_Reading', 'Days_Since_Service',
        'Days_Until_Warranty_Expires', 'Owner_Type', 'Service_History', 'Accident_History',
        'Fuel_Efficiency', 'Fuel_Type_Diesel', 'Fuel_Type_Electric', 'Fuel_Type_Petrol',
        'Maintenance_History_Average', 'Maintenance_History_Good', 'Maintenance_History_Poor',
        'Transmission_Type_Automatic', 'Transmission_Type_Manual',
        'Tire_Condition_Good', 'Tire_Condition_New', 'Tire_Condition_Worn Out',
        'Brake_Condition_Good', 'Brake_Condition_New', 'Brake_Condition_Worn Out',
        'Battery_Status_Good', 'Battery_Status_New', 'Battery_Status_Weak'
    ]

    # Initialize all features to 0
    input_data = {col: 0 for col in feature_columns}

    # Fill numeric fields
    for key in [
        'Mileage', 'Vehicle_Age', 'Engine_Size', 'Odometer_Reading', 'Days_Since_Service',
        'Days_Until_Warranty_Expires', 'Owner_Type', 'Service_History', 'Accident_History', 'Fuel_Efficiency'
    ]:
        input_data[key] = user_input[key]

    # Fill one-hot fields
    input_data[f"Fuel_Type_{user_input['Fuel_Type']}"] = 1
    input_data[f"Maintenance_History_{user_input['Maintenance_History']}"] = 1
    input_data[f"Transmission_Type_{user_input['Transmission_Type']}"] = 1
    input_data[f"Tire_Condition_{user_input['Tire_Condition']}"] = 1
    input_data[f"Brake_Condition_{user_input['Brake_Condition']}"] = 1
    input_data[f"Battery_Status_{user_input['Battery_Status']}"] = 1

    # Create DataFrame
    input_df = pd.DataFrame([input_data])

    # Predict
    prediction = model.predict(input_df)

    print(f"\n🔍 Vehicle: {number_plate.upper()}")
    if prediction[0] == 1:
        print("🚨 Prediction: This vehicle **NEEDS** maintenance.")
    else:
        print("✅ Prediction: This vehicle **does NOT need** maintenance.")
    prediction = model.predict(input_df)[0]

    return prediction  # ✅ Make sure it returns the result (0 or 1)
