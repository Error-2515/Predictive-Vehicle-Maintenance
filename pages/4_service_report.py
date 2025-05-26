import streamlit as st
from datetime import datetime
from register import fetch_vehicle_with_parts, update_part_for_vehicle, update_vehicle_last_serviced

st.set_page_config(page_title="Service Report", layout="wide")
st.title("🔧 Vehicle Service Report")

number_plate = st.text_input("Enter Vehicle Number Plate").upper().strip()

if st.button("Fetch Vehicle"):
    data = fetch_vehicle_with_parts(number_plate)
    
    if data["status"] != "success":
        st.error(data["message"])
    else:
        vehicle = data["vehicle_info"]
        parts = data["parts"]

        st.markdown(f"### Vehicle: {vehicle['number_plate']}")
        st.write(f"Owner: {vehicle['owner_name']}")
        st.write(f"Model: {vehicle['model']}")

        st.markdown("### 🔍 Service Details")
        updated_parts = []

        for part in parts:
            with st.expander(f"🔩 {part['part_name']}"):
                serviced = st.checkbox(f"Serviced `{part['part_name']}`", key=part['part_name'])

                if serviced:
                    service_type = st.radio("Service Type", ["Repaired", "Replaced"], key=f"type_{part['part_name']}")
                    
                    if service_type == "Repaired":
                        part['last_service_date'] = datetime.now().strftime("%Y-%m-%d")
                        updated_parts.append(part)

                    elif service_type == "Replaced":
                        new_date = st.date_input("New Manufacture Date", key=f"manuf_{part['part_name']}")
                        part['manufacture_date'] = new_date.strftime("%Y-%m-%d")
                        part['last_service_date'] = datetime.now().strftime("%Y-%m-%d")
                        updated_parts.append(part)
        # Mechanic Notes Section
        mechanic_note = st.text_area("📝 Mechanic Notes (optional)")

        if st.button("Submit Report"):
            for part in updated_parts:
                update_part_for_vehicle(number_plate, part['part_name'], part)

            update_vehicle_last_serviced(number_plate, mechanic_note)
            st.success("✅ Service report submitted successfully.")


        
