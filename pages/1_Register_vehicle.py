import streamlit as st
from register import register_vehicle_in_tinydb

st.title("📋 Register a New Vehicle")

with st.form("vehicle_form"):
    number_plate = st.text_input("Number Plate")
    owner_name = st.text_input("Owner Name")
    model = st.selectbox("Vehicle Model",['car','truck','bike'])
    make_year = st.number_input("Make Year", min_value=1900, max_value=2100, step=1)
    color = st.text_input("Vehicle Color")
    phone_number = st.text_input("Owner's Phone Number")
    Fuel_Type = st.selectbox("Fuel Type",['Petrol','Diesel','Electric'])
    Transmission_Type = st.selectbox("Transmission Type",['Automatic','Manual'])
    Engine_Size = st.number_input("Engine Size (in cc)", min_value=50, max_value=2500, step=100)
    Odometer_Reading = st.number_input("Odometer Reading", min_value=0, max_value=900000, step=1000)
    Fuel_Efficiency = st.number_input("Fuel Efficiency", min_value=10, max_value=100, step=1)
    Tire_Condition = st.selectbox("Tire Condition",['New','Good','Worn Out'])
    Brake_Condition = st.selectbox("Brake Condition",['New','Good','Worn Out'])
    Battery_Status = st.selectbox("Battery Status",['New','Good','Weak'])
    Owner_Type = st.selectbox("Owner Type",['1','2','3'])
    Accident_History = st.selectbox("No. Of Accidents",['0','1','2','3'])



    submitted = st.form_submit_button("Register Vehicle")
    
    if submitted:
        vehicle_info = {
            "number_plate": number_plate.upper().strip(),
            "owner_name": owner_name,
            "vehicle_type": model,
            "make_year": int(make_year),
            "color": color,
            "phone_number": phone_number,
            "fuel_type": Fuel_Type,
            "transmission_type": Transmission_Type,
            "engine_size": int(Engine_Size),
            "odometer_reading": int(Odometer_Reading),
            "fuel_efficiency": int(Fuel_Efficiency),
            "tire_condition": Tire_Condition,
            "brake_condition": Brake_Condition,
            "battery_status": Battery_Status,
            "owner_type": int(Owner_Type),
            "accident_history": int(Accident_History),
        }
        result = register_vehicle_in_tinydb(vehicle_info)
        if result["status"] == "success":
            st.success(str(result["message"]))
        else:
            st.warning(str(result["message"]))
