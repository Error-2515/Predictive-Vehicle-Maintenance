import streamlit as st
from register import add_part_to_vehicle

st.title("⚙️ Add Part to Vehicle")

with st.form("part_form"):
    number_plate = st.text_input("Enter Registered Number Plate").upper().strip()
    part_name = st.text_input("Part Name")
    manufacture_date = st.date_input("Manufacture Date")
    last_service_date = st.date_input("Last Service Date")
    condition_notes = st.text_area("Condition Notes")
    

    submitted = st.form_submit_button("Add Part")
    if submitted:
        part_info = {
            "part_name": part_name,
            "manufacture_date": manufacture_date.strftime("%Y-%m-%d"),
            "last_service_date": last_service_date.strftime("%Y-%m-%d"),
            "condition_notes": condition_notes
        }
        result = add_part_to_vehicle(number_plate, part_info)
        if result["status"] == "success":
            st.success(str(result["message"]))
        else:
            st.warning(str(result["message"]))
