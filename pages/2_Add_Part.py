import streamlit as st
from register import add_part_to_vehicle

st.title("⚙️ Add Part to Vehicle")

with st.form("part_form"):
    parts=["airfilter","airfilter"]
    number_plate = st.text_input("Enter Registered Number Plate").upper().strip()
    part_name = st.selectbox(label="choose part",options=parts)
    last_service_km=st.number_input("last services (in kms)",min_value=1)
    manufacture_date = st.date_input("Manufacture Date")
    last_service_date = st.date_input("Last Service Date")
    condition_notes = st.text_area("Condition Notes")
    

    submitted = st.form_submit_button("Add Part")
    if submitted:
        part_info = {
            "vehicle_part": part_name,
            "last_service_km":last_service_km,
            "manufacture_date": manufacture_date.strftime("%Y-%m-%d"),
            "last_service_date": last_service_date.strftime("%Y-%m-%d"),
            "condition_notes": condition_notes,
            "RUL_km":""
        }
        result = add_part_to_vehicle(number_plate, part_info)
        if result["status"] == "success":
            st.success(str(result["message"]))
        else:
            st.warning(str(result["message"]))
