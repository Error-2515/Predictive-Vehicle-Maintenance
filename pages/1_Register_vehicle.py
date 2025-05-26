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

    submitted = st.form_submit_button("Register Vehicle")
    if submitted:
        vehicle_info = {
            "number_plate": number_plate.upper().strip(),
            "owner_name": owner_name,
            "model": model,
            "make_year": int(make_year),
            "color": color,
            "phone_number": phone_number
        }
        result = register_vehicle_in_tinydb(vehicle_info)
        if result["status"] == "success":
            st.success(str(result["message"]))
        else:
            st.warning(str(result["message"]))
