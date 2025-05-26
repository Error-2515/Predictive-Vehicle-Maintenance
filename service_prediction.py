from tinydb import TinyDB, Query
import pandas as pd
import joblib

# Load the trained model from the pickle file
model = joblib.load('maintenance_model.pkl')

def predict_from_tinydb(db_path='db.json'):
    # Connect to TinyDB
    db = TinyDB(db_path)
    entries = db.all()

    if not entries:
        print("⚠️ No data found in TinyDB.")
        return

    # Prepare predictions
    for i, entry in enumerate(entries):
        try:
            # Ensure correct feature order as per training
            feature_order = [
                'Mileage', 'Vehicle_Age', 'Engine_Size', 'Odometer_Reading',
                'Days_Since_Service', 'Days_Until_Warranty_Expires', 'Owner_Type',
                'Service_History', 'Accident_History', 'Fuel_Efficiency',
                'Fuel_Type_Diesel', 'Fuel_Type_Electric', 'Fuel_Type_Petrol',
                'Maintenance_History_Average', 'Maintenance_History_Good', 'Maintenance_History_Poor',
                'Transmission_Type_Automatic', 'Transmission_Type_Manual',
                'Tire_Condition_Good', 'Tire_Condition_New', 'Tire_Condition_Worn Out',
                'Brake_Condition_Good', 'Brake_Condition_New', 'Brake_Condition_Worn Out',
                'Battery_Status_Good', 'Battery_Status_New', 'Battery_Status_Weak'
            ]

            # Create a DataFrame with a single row in correct order
            input_df = pd.DataFrame([[entry[feature] for feature in feature_order]], columns=feature_order)

            # Predict
            prediction = model.predict(input_df)[0]

            # Output
            print(f"🔎 Entry {i+1}: Maintenance Required? {'Yes' if prediction == 1 else 'No'}")

        except KeyError as e:
            print(f"❌ Missing key in entry {i+1}: {e}")
        except Exception as e:
            print(f"❌ Error processing entry {i+1}: {e}")