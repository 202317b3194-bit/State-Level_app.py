import streamlit as st
import pandas as pd

# =====================================================
# Page Configuration
# =====================================================
st.set_page_config(
    page_title="State Level Real Estate View",
    layout="wide"
)

# =====================================================
# Load Data (CSV ONLY)
# =====================================================
@st.cache_data
def load_data():
    df = pd.read_csv("City_level_Data.csv")

    # Clean column names (important)
    df.columns = df.columns.str.strip()

    return df


df = load_data()

# =====================================================
# App Title
# =====================================================
st.title("🏠 State‑Level Real Estate Insights")
st.caption("State → City → Locality drill‑down analysis")

# =====================================================
# Validate Required Columns
# =====================================================
required_cols = [
    "State",
    "City",
    "Locality",
    "BHK",
    "Area_sqft",
    "Price_per_Sqft",
    "House_Price_Lakh",
    "Rental_Yield"
]

missing_cols = [c for c in required_cols if c not in df.columns]

if missing_cols:
    st.error(f"Missing columns in CSV: {missing_cols}")
    st.stop()

# =====================================================
# State Selection
# =====================================================
states = sorted(df["State"].dropna().unique())

selected_state = st.selectbox(
    "Select State",
    states
)

state_df = df[df["State"] == selected_state]

# =====================================================
# State KPIs
# =====================================================
st.subheader(f"📊 {selected_state} – Key Metrics")

k1, k2, k3, k4 = st.columns(4)

k1.metric(
    "Avg Price / Sqft",
    f"₹ {state_df['Price_per_Sqft'].mean():,.0f}"
)

k2.metric(
    "Avg House Price",
    f"₹ {state_df['House_Price_Lakh'].mean():.1f} L"
)

k3.metric(
    "Avg Rental Yield",
    f"{state_df['Rental_Yield'].mean():.2f}%"
)

k4.metric(
    "Total Listings",
    len(state_df)
)

# =====================================================
# City Selection
# =====================================================
st.subheader("🏙 City‑Level View")

cities = sorted(state_df["City"].dropna().unique())

selected_city = st.selectbox(
    "Select City",
    cities
)

city_df = state_df[state_df["City"] == selected_city]

# =====================================================
# City KPIs
# =====================================================
c1, c2, c3 = st.columns(3)

c1.metric("Listings", len(city_df))
c2.metric(
    "Avg Price / Sqft",
    f"₹ {city_df['Price_per_Sqft'].mean():,.0f}"
)
c3.metric(
    "Avg BHK",
    f"{city_df['BHK'].mean():.1f}"
)

# =====================================================
# Price Distribution Chart
# =====================================================
st.subheader(f"📈 {selected_city} – Price per Sqft Distribution")

st.bar_chart(
    city_df.groupby("Locality")["Price_per_Sqft"]
    .mean()
    .sort_values(ascending=False)
)

# =====================================================
# Locality-Level Table
# =====================================================
st.subheader(f"📍 {selected_city} – Property Listings")

display_cols = [
    "Locality",
    "BHK",
    "Area_sqft",
    "Price_per_Sqft",
    "House_Price_Lakh",
    "Rental_Yield"
]

st.dataframe(
    city_df[display_cols]
    .sort_values("Price_per_Sqft", ascending=False)
    .reset_index(drop=True),
    use_container_width=True
)

# =====================================================
# Footer
# =====================================================
st.markdown("---")
st.caption("State-Level Real Estate Dashboard | Streamlit")
