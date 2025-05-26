import sklearn
import pandas as pd
df = pd.read_csv('vehicle_maintenance_data.csv', on_bad_lines='warn')
df['Transmission_Type'].fillna(df['Transmission_Type'].mode()[0], inplace=True)
df['Engine_Size'].fillna(df['Engine_Size'].mean(), inplace=True)
df['Odometer_Reading'].fillna(df['Odometer_Reading'].mean(), inplace=True)
df['Last_Service_Date'].fillna(df['Last_Service_Date'].mode()[0], inplace=True)
df['Warranty_Expiry_Date'].fillna(df['Warranty_Expiry_Date'].mode()[0], inplace=True)
df['Owner_Type'].fillna(df['Owner_Type'].mode()[0], inplace=True)
df['Insurance_Premium'].fillna(df['Insurance_Premium'].mean(), inplace=True)
df['Service_History'].fillna(df['Service_History'].mode()[0], inplace=True)
df['Accident_History'].fillna(df['Accident_History'].mode()[0], inplace=True)
df['Fuel_Efficiency'].fillna(df['Fuel_Efficiency'].mean(), inplace=True)
df['Tire_Condition'].fillna(df['Tire_Condition'].mode()[0], inplace=True)
df['Brake_Condition'].fillna(df['Brake_Condition'].mode()[0], inplace=True)
df['Battery_Status'].fillna(df['Battery_Status'].mode()[0], inplace=True)
df['Need_Maintenance'].fillna(df['Need_Maintenance'].mode()[0], inplace=True)
df['Last_Service_Date'] = pd.to_datetime(df['Last_Service_Date'], errors='coerce')
df['Days_Since_Service'] = (pd.Timestamp.now() - df['Last_Service_Date']).dt.days
df['Warranty_Expiry_Date'] = pd.to_datetime(df['Warranty_Expiry_Date'], errors='coerce')
df['Days_Until_Warranty_Expires'] = (df['Warranty_Expiry_Date'] - pd.Timestamp.now()).dt.days
df = pd.get_dummies(df, columns=['Fuel_Type'], prefix='Fuel_Type')
cols = ['Fuel_Type_Diesel', 'Fuel_Type_Petrol', 'Fuel_Type_Electric']
df[cols] = df[cols].astype(int)
df = pd.get_dummies(df, columns=['Maintenance_History'], prefix='Maintenance_History')
cols = ['Maintenance_History_Average', 'Maintenance_History_Good', 'Maintenance_History_Poor']
df[cols] = df[cols].astype(int)
df = pd.get_dummies(df, columns=['Transmission_Type'], prefix='Transmission_Type')
cols = ['Transmission_Type_Automatic', 'Transmission_Type_Manual']
df[cols] = df[cols].astype(int)
from sklearn.preprocessing import LabelEncoder

le = LabelEncoder()
df['Owner_Type'] = le.fit_transform(df['Owner_Type'])
df = pd.get_dummies(df, columns=['Tire_Condition'], prefix='Tire_Condition')
cols = ['Tire_Condition_Good', 'Tire_Condition_New', 'Tire_Condition_Worn Out']
df[cols] = df[cols].astype(int)
df = pd.get_dummies(df, columns=['Brake_Condition'], prefix='Brake_Condition')
cols = ['Brake_Condition_Good', 'Brake_Condition_New', 'Brake_Condition_Worn Out']
df[cols] = df[cols].astype(int)
df = pd.get_dummies(df, columns=['Battery_Status'], prefix='Battery_Status')
cols = ['Battery_Status_Good', 'Battery_Status_New', 'Battery_Status_Weak']
df[cols] = df[cols].astype(int)
X = df[['Mileage', 'Vehicle_Age', 'Engine_Size', 'Odometer_Reading', 'Days_Since_Service', 'Days_Until_Warranty_Expires', 'Owner_Type', 'Service_History', 'Accident_History', 'Fuel_Efficiency', 'Fuel_Type_Diesel', 'Fuel_Type_Electric', 'Fuel_Type_Petrol', 'Maintenance_History_Average', 'Maintenance_History_Good', 'Maintenance_History_Poor', 'Transmission_Type_Automatic', 'Transmission_Type_Manual', 'Tire_Condition_Good', 'Tire_Condition_New', 'Tire_Condition_Worn Out', 'Brake_Condition_Good', 'Brake_Condition_New', 'Brake_Condition_Worn Out', 'Battery_Status_Good', 'Battery_Status_New', 'Battery_Status_Weak']]
y = df['Need_Maintenance']
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(
    X, y,                # your features and target
    test_size=0.2,       # 20% for testing, 80% for training
    random_state=42      # for consistent results every time you run it
)
from sklearn.ensemble import RandomForestClassifier
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
from sklearn.metrics import accuracy_score

accuracy = accuracy_score(y_test, y_pred)
print("Model Accuracy:", accuracy)
from sklearn.metrics import confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

# Predict on the test set
y_pred = model.predict(X_test)

# Create confusion matrix
cm = confusion_matrix(y_test, y_pred)

# Plot it
plt.figure(figsize=(6,4))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=[0,1], yticklabels=[0,1])
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix')
plt.show()

import pandas as pd

# Step 1: Define the prediction function
def predict_maintenance_terminal(model):
    print("🔧 Enter vehicle details below:")
    
    # Step 2: Get input from the user
    user_input = {
        'Mileage': float(input("Mileage: ")),
        'Vehicle_Age': float(input("Vehicle Age (years): ")),
        'Engine_Size': float(input("Engine Size (L): ")),
        'Odometer_Reading': float(input("Odometer Reading: ")),
        'Days_Since_Service': int(input("Days Since Last Service: ")),
        'Days_Until_Warranty_Expires': int(input("Days Until Warranty Expires: ")),
        'Owner_Type': int(input("Owner Type (1: First, 2: Second, etc.): ")),
        'Service_History': int(input("Service History (e.g., 1 to 5): ")),
        'Accident_History': int(input("Number of Accidents Reported: ")),
        'Fuel_Efficiency': float(input("Fuel Efficiency (km/l): ")),

        'Fuel_Type': input("Fuel Type (Diesel / Petrol / Electric): ").title(),
        'Maintenance_History': input("Maintenance History (Good / Average / Poor): ").title(),
        'Transmission_Type': input("Transmission Type (Automatic / Manual): ").title(),
        'Tire_Condition': input("Tire Condition (New / Good / Worn Out): ").title(),
        'Brake_Condition': input("Brake Condition (New / Good / Worn Out): ").title(),
        'Battery_Status': input("Battery Status (New / Good / Weak): ").title()
    }

    # Step 3: Prepare feature columns
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

    # Step 4: Initialize all features with 0
    input_data = {col: 0 for col in feature_columns}

    # Step 5: Fill numeric fields
    for key in [
        'Mileage', 'Vehicle_Age', 'Engine_Size', 'Odometer_Reading', 'Days_Since_Service',
        'Days_Until_Warranty_Expires', 'Owner_Type', 'Service_History', 'Accident_History', 'Fuel_Efficiency'
    ]:
        input_data[key] = user_input[key]

    # Step 6: Fill one-hot fields
    input_data[f"Fuel_Type_{user_input['Fuel_Type']}"] = 1
    input_data[f"Maintenance_History_{user_input['Maintenance_History']}"] = 1
    input_data[f"Transmission_Type_{user_input['Transmission_Type']}"] = 1
    input_data[f"Tire_Condition_{user_input['Tire_Condition']}"] = 1
    input_data[f"Brake_Condition_{user_input['Brake_Condition']}"] = 1
    input_data[f"Battery_Status_{user_input['Battery_Status']}"] = 1

    # Step 7: Create DataFrame for model
    input_df = pd.DataFrame([input_data])

    # Step 8: Predict using trained model
    prediction = model.predict(input_df)

    # Step 9: Display prediction
    print("\n🔍 Prediction Result:")
    if prediction[0] == 1:
        print("🚨 Vehicle *NEEDS* maintenance.")
    else:
        print("✅ Vehicle does *NOT* need maintenance.")
# model='maintenance_model.pkl'
predict_maintenance_terminal(model)
import joblib

# After training your model
joblib.dump(model, 'maintenance_model.pkl')