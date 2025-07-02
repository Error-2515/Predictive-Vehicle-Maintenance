import streamlit as st
from register import add_part_to_vehicle, fetch_vehicle_with_parts

st.title("⚙️ Add Part to Vehicle")
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] {
        display: none;
    }
    </style>
    """, unsafe_allow_html=True)
with st.sidebar:
    
    st.markdown(
    """
    <div style='padding:20px;'></div>
    """,unsafe_allow_html=True)
    st.page_link("pages/1_Register_vehicle.py", label="📊 Vehicle Dashboard")
    st.page_link("pages/2_Add_Part.py", label="⚙️ Add Parts")
    st.page_link("pages/3_View_Vehicle_Dashboard.py", label="📈 Vehicle Dashboard")
    st.page_link("pages/4_service_report.py", label="🧰 Service Report")

    
with st.form("part_form"):
    parts = ["air filter", "battery", "brake pads", "clutch", "engine", "gearbox", "suspension", "tires"]
    number_plate = st.text_input("Enter Registered Number Plate").upper().strip()
    part_name = st.selectbox(label="Choose Part", options=parts)
    last_service_km = st.number_input("Last Service (in kms)", min_value=1)
    manufacture_date = st.date_input("Manufacture Date")
    last_service_date = st.date_input("Last Service Date")
    condition_notes = st.text_area("Condition Notes")

    submitted = st.form_submit_button("Add Part")
    if submitted:
        # 🛑 Check if the part already exists
        vehicle_data = fetch_vehicle_with_parts(number_plate)
        if vehicle_data["status"] != "success":
            st.warning(vehicle_data["message"])
        else:
            existing_parts = vehicle_data["parts"]
            existing_part_names = [p["vehicle_part"].lower() for p in existing_parts]

            if part_name.lower() in existing_part_names:
                st.error(f"❌ Part '{part_name}' already exists for this vehicle.")
            else:
                part_info = {
                    "vehicle_part": part_name,
                    "last_service_km": last_service_km,
                    "manufacture_date": manufacture_date.strftime("%Y-%m-%d"),
                    "last_service_date": last_service_date.strftime("%Y-%m-%d"),
                    "condition_notes": condition_notes,
                    "RUL_km": ""
                }
                result = add_part_to_vehicle(number_plate, part_info)
                if result["status"] == "success":
                    st.success(result["message"])
                else:
                    st.warning(result["message"])
