import streamlit as st
from register import register_vehicle_in_tinydb

st.title("📋 Register a New Vehicle")

with st.form("vehicle_form"):
    number_plate = st.text_input("Number Plate")
    owner_name = st.text_input("Owner Name")
    model = st.text_input("Vehicle Model")
    make_year = st.number_input("Make Year", min_value=1900, max_value=2100, step=1)
    color = st.text_input("Vehicle Color")
    phone_number = st.text_input("Owner's Phone Number")
    Fuel_Type = st.text_input("Fuel Type")
    Transmission_Type = st.text_input("Transmission Type")
    Engine_Size = st.number_input("Engine Size (in cc)", min_value=50, max_value=2500, step=100)
    Odometer_Reading = st.number_input("Odometer Reading", min_value=0, max_value=200000, step=1000)
    Fuel_Efficiency = st.number_input("Fuel Efficiency", min_value=10, max_value=100, step=1)
    Tire_Condition = st.text_input("Tire Condition")
    Brake_Condition = st.text_input("Brake Condition")
    Battery_Status = st.text_input("Battery Status")
    Owner_Type = st.number_input("Owner Type", min_value=1, max_value=10, step=1)
    Accident_History = st.number_input("No. Of Accidents", min_value=1, max_value=5, step=1)



    submitted = st.form_submit_button("Register Vehicle")
    
    if submitted:
        vehicle_info = {
            "number_plate": number_plate.upper().strip(),
            "owner_name": owner_name,
            "model": model,
            "make_year": int(make_year),
            "color": color,
            "phone_number": phone_number,
            "Fuel_Type": Fuel_Type,
            "Transmission_Type": Transmission_Type,
            "Engine_Size": int(Engine_Size),
            "Odometer_Reading": int(Odometer_Reading),
            "Fuel_Efficiency": int(Fuel_Efficiency),
            "Tire_Condition": Tire_Condition,
            "Brake_Condition": Brake_Condition,
            "Battery_Status": Battery_Status,
            "Owner_Type": int(Owner_Type),
            "Accident_History": int(Accident_History),
        }
        result = register_vehicle_in_tinydb(vehicle_info)
        if result["status"] == "success":
            st.success(str(result["message"]))
        else:
            st.warning(str(result["message"]))
