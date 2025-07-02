import streamlit as st
from register import fetch_vehicle_with_parts
import pandas as pd
from pmv import predict_by_number_plate
from RUL_prediction import predict_rul_from_db
st.title("📊 Vehicle Dashboard")
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

    
number_plate = st.text_input("Enter Number Plate to Search").upper().strip()
if st.button("Search"):
    result = fetch_vehicle_with_parts(number_plate)
    rul_return=predict_rul_from_db(number_plate)
    print(rul_return)
    if result["status"] == "success":
        vehicle = result["vehicle_info"]
        parts = result["parts"]

        st.markdown(f"### Vehicle Number: \n### {vehicle['number_plate']}")

        st.markdown("### Vehicle Information:")
        st.write(f"**Owner:** {vehicle['owner_name']}")
        st.write(f"**Model:** {vehicle['vehicle_type']}")
        st.write(f"**Make Year:** {vehicle['make_year']}")
        st.write(f"**Color:** {vehicle['color']}")
        st.write(f"**Phone:** {vehicle['phone_number']}")
        st.write(f"**Ododmeter:** {vehicle['odometer_reading']}")
        # 🔍 Predict maintenance using function from pmv.py
        prediction = predict_by_number_plate(number_plate)
        # Add this after fetching `vehicle`:
        if "last_mechanic_note" in vehicle and vehicle["last_mechanic_note"]:
            st.markdown("### 📝 Last Mechanic Note")
            st.write(vehicle["last_mechanic_note"])
        st.markdown("### Vehicle service prediction:")
        # ✅ Display result
        if prediction == 1:
            st.write("🚨 This vehicle **NEEDS maintenance**.")
        else:
            st.write("✅ This vehicle **does NOT need maintenance**.")

        st.markdown("---")
        st.subheader("🛠️ Parts Information")

        if parts:
            # Create a DataFrame for parts
            parts_data = []
            for part in parts:
                # try:
                #     rul_km = float(part.get("RUL_km", None))
                # except (ValueError, TypeError):
                #     rul_km = None  # Or 0 if you want a numeric fallback

                parts_data.append({
                    "vehicle_part": part.get("vehicle_part", "Unknown"),
                    "last_service_km": part.get("last_service_km", "N/A"),
                    "Manufacture Date": part.get("manufacture_date", "N/A"),
                    "Last Service Date": part.get("last_service_date", "N/A"),
                    "Condition Notes": part.get("condition_notes", ""),
                    "Days Since Last Service": part.get("days_since_service", "N/A"),
                    "RUL_km": part.get("RUL_km",None)
                })
            df_parts = pd.DataFrame(parts_data)
            st.dataframe(df_parts)
        else:
            st.info("No parts added yet.")
    else:
        st.error(str(result["message"]))
