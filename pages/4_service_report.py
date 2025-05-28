import streamlit as st
from datetime import datetime
from register import (
    fetch_vehicle_with_parts,
    update_part_for_vehicle,
    update_vehicle_last_serviced,
    update_vehicle_odometer
)

st.set_page_config(page_title="Service Report", layout="wide")
st.title("🔧 Vehicle Service Report")

number_plate = st.text_input("Enter Vehicle Number Plate").upper().strip()

# Step 1: Fetch vehicle
if st.button("Fetch Vehicle"):
    data = fetch_vehicle_with_parts(number_plate)
    if data["status"] != "success":
        st.error(data["message"])
    else:
        st.session_state['vehicle_data'] = data

# Step 2: Process and show form
if 'vehicle_data' in st.session_state:
    data = st.session_state['vehicle_data']
    vehicle = data["vehicle_info"]
    parts = data["parts"]

    st.markdown(f"### Vehicle: {vehicle['number_plate']}")
    st.write(f"Owner: {vehicle['owner_name']}")
    st.write(f"Model: {vehicle['vehicle_type']}")
    st.write(f"Previous Odometer Reading: {vehicle.get('Odometer_Reading', 'N/A')} km")

    # 🔢 Input for current odometer reading
    current_km = st.number_input("Enter Current Odometer Reading (in km)", min_value=0, value=int(vehicle.get("Odometer_Reading", 0)))

    st.markdown("### 🔍 Service Details")
    updated_parts = []
    any_serviced = False

    for part in parts:
        with st.expander(f"🔩 {part['vehicle_part']}"):
            key_prefix = f"{number_plate}_{part['vehicle_part']}"
            serviced = st.checkbox(f"Serviced `{part['vehicle_part']}`", key=f"{key_prefix}_serviced")

            if serviced:
                any_serviced = True
                service_type = st.radio("Service Type", ["Repaired", "Replaced"], key=f"{key_prefix}_type")

                part['last_service_date'] = datetime.now().strftime("%Y-%m-%d")
                part['last_service_km'] = current_km  # ✅ Set to odometer

                if service_type == "Replaced":
                    new_date = st.date_input("New Manufacture Date", key=f"{key_prefix}_manuf")
                    part['manufacture_date'] = new_date.strftime("%Y-%m-%d")

                updated_parts.append(part)

    # 📝 Optional mechanic notes
    mechanic_note = st.text_area("📝 Mechanic Notes (optional)")

    # Step 3: Submit updates
    if st.button("Submit Report"):
        for part in updated_parts:
            update_part_for_vehicle(vehicle['number_plate'], part['vehicle_part'], part)

        if any_serviced:
            update_vehicle_last_serviced(vehicle['number_plate'], mechanic_note)
            update_vehicle_odometer(vehicle['number_plate'], current_km)  # ✅ Update main odometer

        st.success("✅ Service report submitted successfully.")
        del st.session_state['vehicle_data']  # Clear state after submission
