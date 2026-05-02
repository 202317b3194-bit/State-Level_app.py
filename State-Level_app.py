import streamlit as st
import pandas as pd
# --------------------------------------------------
# Page config
# --------------------------------------------------
st.set_page_config(
    page_title="State Level Real Estate View",
    layout="wide"
)
# --------------------------------------------------
# Load data
# --------------------------------------------------
@st.cache_data
def load_data():
    state_df = pd.read_excel(
        "Real_estate_data_India 2.xlsx",
        sheet_name=0,  # State-level sheet
        engine="openpyxl"
    )
    city_df = pd.read_excel(
        "Real_estate_data_India 2.xlsx",
        sheet_name="City Level",
        engine="openpyxl"
    )
    return state_df, city_df

state_df, city_df = load_data()
# --------------------------------------------------
# Title
# --------------------------------------------------
st.title("🏠 State‑Level Real Estate Insights")
st.markdown("Drill down from **State → City** using the Indian real estate dataset.")
# --------------------------------------------------
# State selection
# --------------------------------------------------
states = sorted(state_df["State / Union Territory"].unique())
selected_state = st.selectbox(
    "Select State / Union Territory",
    states
)
# --------------------------------------------------
# Filter selected state
# --------------------------------------------------
state_data = state_df[
    state_df["State / Union Territory"] == selected_state
]
# --------------------------------------------------
# KPI Section (State level)
# --------------------------------------------------
st.subheader(f"📊 {selected_state} – Key Metrics")
if not state_data.empty:
    r = state_data.iloc[0]
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric(
        "Median House Price (2025)",
        f"₹ {r['Median House Price (₹ Lakh) -2025']:.2f} L"
    )
    kpi2.metric(
        "Price / Sqft",
        f"₹ {int(r['Price/sqft (₹)'])}"
    )
    kpi3.metric(
        "YoY Growth",
        f"{r['YoY Price Growth (%)'] * 100:.1f}%"
    )
    kpi4.metric(
        "Price‑Income Ratio",
        f"{r['Price-to-Income Ratio']:.2f}"
    )
    st.caption(
        f"**Market Tier:** {r['Market Tier']} | "
        f"**Region:** {r['Region']} | "
        f"**Proximity:** {r['Proximity Category']}"
    )
# --------------------------------------------------
# City mapping (simple & reliable for demo)
# --------------------------------------------------
STATE_CITY_MAP = {
    "Tamil Nadu": ["Chennai", "Madurai"],
    "Telangana": ["Hyderabad"],
    "Maharashtra": ["Mumbai"],
    "Delhi (NCR)": ["New Delhi", "Gurugram"],
    "Karnataka": ["Bengaluru"],
    "Uttar Pradesh": ["Lucknow"],
    "West Bengal": ["Kolkata"],
    "Gujarat": ["Ahmedabad"],
    "Kerala": ["Kochi"],
    "Rajasthan": ["Jaipur"],
    "Punjab": ["Amritsar"],
    "Bihar": ["Patna"],
    "Odisha": ["Bhubaneswar"],
    "Jharkhand": ["Ranchi"],
    "Chhattisgarh": ["Raipur"],
    "Assam": ["Dispur"],
    "Goa": ["Panaji"],
    "Himachal Pradesh": ["Shimla"],
    "Jammu & Kashmir": ["Srinagar"],
    "Puducherry (UT)": ["Puducherry"],
    "Chandigarh (UT)": ["Chandigarh"],
    "Andhra Pradesh": ["Vijayawada"],
    "Sikkim": ["Gangtok"],
    "Tripura": ["Agartala"],
    "Nagaland": ["Kohima"],
    "Manipur": ["Imphal"],
    "Meghalaya": ["Shillong"],
    "Arunachal Pradesh": ["Itanagar"],
    "A & N Islands": ["Port Blair"],
    "Lakshadweep (UT)": ["Kavaratti"],
    "Ladakh (UT)": ["Leh Market"]
}
cities_in_state = STATE_CITY_MAP.get(selected_state, [])
# --------------------------------------------------
# City section
# --------------------------------------------------
st.subheader("🏙 City‑Level Drill‑Down")
if len(cities_in_state) == 0:
    st.warning("No city mapping available for this state.")
else:
    selected_city = st.selectbox(
        "Select City",
        sorted(cities_in_state)
    )
    city_data = city_df[city_df["City"] == selected_city]
    if city_data.empty:
        st.info("No city‑level listings found.")
    else:
        c1, c2, c3 = st.columns(3)
        c1.metric(
            "Total Listings",
            len(city_data)
        )
        c2.metric(
            "Avg Price / Sqft",
            f"₹ {city_data['Price per Sqft (INR)S'].mean():,.0f}"
        )
        c3.metric(
            "Avg Rental Yield",
            f"{city_data['Rental Yield (%)'].mean():.2f}%"
        )
        # --------------------------------------------------
        # Locality table
        # --------------------------------------------------
        st.markdown("### 📍 Locality‑Level Listings")
        table_cols = [
            "Locality",
            "Built-up Area (sqft)",
            "Price per Sqft (INR)S",
            "Bedrooms (BHK)",
            "Bathrooms",
            "Furnishing Status",
            "Rental Yield (%)",
            "Estimated Sale Price (INR)"
        ]
        st.dataframe(
            city_data[table_cols]
            .sort_values("Price per Sqft (INR)S", ascending=False)
            .reset_index(drop=True),
            use_container_width=True
        )
# --------------------------------------------------
# Footer
# --------------------------------------------------
st.markdown("---")
st.caption("State → City real estate view | Streamlit dashboard")
