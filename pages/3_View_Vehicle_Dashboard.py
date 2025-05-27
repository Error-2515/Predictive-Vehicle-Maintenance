import streamlit as st
from register import fetch_vehicle_with_parts
import pandas as pd
from pmv import predict_by_number_plate
st.title("📊 Vehicle Dashboard")

number_plate = st.text_input("Enter Number Plate to Search").upper().strip()
if st.button("Search"):
    result = fetch_vehicle_with_parts(number_plate)
    if result["status"] == "success":
        vehicle = result["vehicle_info"]
        parts = result["parts"]

        st.markdown(f"### Vehicle: {vehicle['number_plate']}")

        st.subheader("Vehicle Information")
        st.write(f"**Owner:** {vehicle['owner_name']}")
        st.write(f"**Model:** {vehicle['model']}")
        st.write(f"**Make Year:** {vehicle['make_year']}")
        st.write(f"**Color:** {vehicle['color']}")
        st.write(f"**Phone:** {vehicle['phone_number']}")
        # 🔍 Predict maintenance using function from pmv.py
        prediction = predict_by_number_plate(number_plate)

        # ✅ Display result
        if prediction == 1:
            st.title("🚨 This vehicle **NEEDS maintenance**.")
        else:
            st.title("✅ This vehicle **does NOT need maintenance**.")

        st.markdown("---")
        st.subheader("🛠️ Parts Information")

        if parts:
            # Create a DataFrame for parts
            parts_data = []
            for part in parts:
                parts_data.append({
                    "Part Name": part["part_name"],
                    "Manufacture Date": part["manufacture_date"],
                    "Last Service Date": part["last_service_date"],
                    "Condition Notes": part["condition_notes"],
                    "Days Since Last Service": part.get("days_since_service", "N/A")
                })
            
            df_parts = pd.DataFrame(parts_data)
            st.dataframe(df_parts)
        else:
            st.info("No parts added yet.")
    else:
        st.error(str(result["message"]))
