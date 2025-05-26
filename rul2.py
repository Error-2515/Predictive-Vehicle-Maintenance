import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
import numpy as np

# Load your dataset
df = pd.read_csv("rul.csv")  # Replace with your file

# Encode categorical columns
label_encoders = {}
for col in ['vehicle_type', 'vehicle_part']:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le

# Define features and target
X = df[['vehicle_type', 'vehicle_part', 'total_km', 'last_service_km']]
y = df['RUL_km']

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Predict and evaluate
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print("Model Evaluation Metrics:")
print(f"  Mean Absolute Error (MAE): {mae:.2f}")
print(f"  Root Mean Squared Error (RMSE): {rmse:.2f}")
print(f"  R^2 Score: {r2:.3f}")

# Save model
joblib.dump(model, "vehicle_rul_model.pkl")
print("\n✅ Model saved as 'vehicle_rul_model.pkl'")


# ---------- MAIN PART FOR USER INPUT ----------

def predict_rul_input():
    print("\n--- Predict Remaining Useful Life (RUL) ---")
    # Get user input
    vehicle_type_input = input("Enter vehicle type: ").strip().lower()
    vehicle_part_input = input("Enter vehicle part: ").strip().lower()
    total_km = float(input("Enter total kilometers driven: "))
    last_service = float(input("Enter kilometers at last service: "))

    # Encode categorical inputs
    if vehicle_type_input not in label_encoders['vehicle_type'].classes_:
        print("❌ Unknown vehicle type.")
        return
    if vehicle_part_input not in label_encoders['vehicle_part'].classes_:
        print("❌ Unknown vehicle part.")
        return

    vehicle_type_encoded = label_encoders['vehicle_type'].transform([vehicle_type_input])[0]
    vehicle_part_encoded = label_encoders['vehicle_part'].transform([vehicle_part_input])[0]

    # Prepare input
    input_df = pd.DataFrame([{
        'vehicle_type': vehicle_type_encoded,
        'vehicle_part': vehicle_part_encoded,
        'total_km': total_km,
        'last_service_km': last_service
    }])

    # Load model
    loaded_model = joblib.load("vehicle_rul_model.pkl")
    prediction = loaded_model.predict(input_df)[0]
    print(f"\n🔧 Predicted RUL: {int(prediction)} kilometers")

# Run prediction if script is executed directly
if __name__ == "__main__":
    predict_rul_input()
