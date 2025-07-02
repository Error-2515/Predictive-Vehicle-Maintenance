import streamlit as st

st.set_page_config(page_title="Predictive Maintenance", layout="wide")
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] {
        display: none;
    }
    </style>
    """, unsafe_allow_html=True)
st.title("🚗 Predictive Vehicle Maintenance System")

st.markdown("""
Welcome to the **Predictive Vehicle Maintenance System** – an intelligent platform designed to help you manage and maintain vehicles efficiently by predicting part failures, tracking service history, and improving overall vehicle health.

---

### 🔧 Key Features of This Application

Use the **sidebar** to navigate between the different modules:

- **📊 Vehicle Dashboard**  
  View comprehensive details of any registered vehicle, including ownership, odometer readings, and current maintenance status. It also shows part-wise RUL (Remaining Useful Life) predictions and alerts if the vehicle needs maintenance.

- **⚙️ Add Parts**  
  Register new parts for a vehicle, such as brakes, engine, battery, etc., along with their service history and manufacture details. The system ensures duplicate parts aren't added for the same vehicle.

- **🧰 Service Report**  
  Update a vehicle’s service history by logging recent repairs or replacements. Enter the current odometer reading, select which parts were serviced, and leave optional mechanic notes. The system automatically updates part service dates and the vehicle's last serviced status.

- **📈 Predict RUL (Remaining Useful Life)**  
  Run machine learning-powered predictions to estimate how long each part can last before needing service or replacement. This helps in proactive maintenance planning.

---

### ✅ How It Works

1. **Register and manage vehicles** – Store detailed information including type, make year, engine specs, and ownership.
2. **Track parts** – Every vehicle can have multiple parts associated with it, each with their own service metadata.
3. **Service Logging** – Mechanics can log service events and update parts with notes, dates, and odometer data.
4. **AI Predictions** – The system uses trained models to predict how much longer a part will last based on vehicle and part usage history.

---

🔍 Navigate using the **sidebar** on the left to get started!
""")


with st.sidebar:
    
    st.markdown(
    """
    <div style='padding:20px;'></div>
    """,unsafe_allow_html=True)
    st.page_link("pages/1_Register_vehicle.py", label="📊 Vehicle Dashboard")
    st.page_link("pages/2_Add_Part.py", label="⚙️ Add Parts")
    st.page_link("pages/3_View_Vehicle_Dashboard.py", label="📈 Vehicle Dashboard")
    st.page_link("pages/4_service_report.py", label="🧰 Service Report")

    
