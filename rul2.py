import streamlit as st
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

# Load dataset
df = pd.read_csv("vehicle_rul_dataset.csv")

# Encode categorical columns
label_encoders = {}
for col in ['terrain', 'brake_score', 'vehicle_type']:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le

# Features and label
X = df.drop(columns=['vehicle_id', 'RUL_km'])
y = df['RUL_km']

# Train model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X, y)

# Streamlit UI
st.title("Vehicle RUL Predictor")

st.markdown("Enter the following vehicle details:")

total_km = st.number_input("Total kilometers driven", min_value=0, step=100)
avg_trip_km = st.number_input("Average trip length (in km)", min_value=0.0, step=1.0)
trips_per_day = st.number_input("Average trips per day", min_value=0, step=1)
last_replacement_km = st.number_input("Kilometers at last replacement", min_value=0, step=100)

terrain_input = st.selectbox("Terrain", options=['flat', 'hilly'])
urban_ratio = st.slider("Urban driving ratio", min_value=0.0, max_value=1.0, step=0.01)
brake_score_input = st.selectbox("Brake Score", options=['low', 'medium', 'high'])
vehicle_type_input = st.selectbox("Vehicle Type", options=['sedan', 'SUV', 'hatchback'])

# When Submit is clicked
if st.button("Predict RUL"):
    # Encode inputs
    terrain = label_encoders['terrain'].transform([terrain_input])[0]
    brake_score = label_encoders['brake_score'].transform([brake_score_input])[0]
    vehicle_type = label_encoders['vehicle_type'].transform([vehicle_type_input])[0]

    input_data = pd.DataFrame([{
        'total_km': total_km,
        'avg_trip_km': avg_trip_km,
        'trips_per_day': trips_per_day,
        'last_replacement_km': last_replacement_km,
        'terrain': terrain,
        'urban_ratio': urban_ratio,
        'brake_score': brake_score,
        'vehicle_type': vehicle_type
    }])

    prediction = model.predict(input_data)[0]
    st.success(f"Predicted Remaining Useful Life (RUL): {int(prediction)} kilometers")