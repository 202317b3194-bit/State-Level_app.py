import streamlit as st
import pandas as pd

# -------------------------------------------------
# Page Configuration
# -------------------------------------------------
st.set_page_config(
    page_title="State-Level Real Estate Dashboard",
    layout="wide"
)

# -------------------------------------------------
# Load Data (CSV – EXACT filename & case)
# -------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("City_level_data.csv")
    df.columns = df.columns.str.strip()  # Clean column names
    return df


df = load_data()

# -------------------------------------------------
# App Title
# -------------------------------------------------
st.title("🏠 State‑Level Real Estate Insights")
st.caption("Person‑2 | State → City drill‑down view")

# -------------------------------------------------
# Required Columns Validation
# -------------------------------------------------
required_columns = [
    "State",
    "City",
    "Locality",
    "BHK",
    "Area_sqft",
    "Price_per_Sqft",
    "House_Price_Lakh",
    "Rental_Yield"
]

missing_cols = [col for col in required_columns if col not in df.columns]

if missing_cols:
    st.error(f"Missing required columns in CSV: {missing_cols}")
    st.stop()

# -------------------------------------------------
# State Selection
# -------------------------------------------------
states = sorted(df["State"].dropna().unique())

selected_state = st.selectbox(
    "Select State",
    states
)

state_df = df[df["State"] == selected_state]

# -------------------------------------------------
# State‑Level KPIs
# -------------------------------------------------
st.subheader(f"📊 {selected_state} – State Metrics")

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

# -------------------------------------------------
# City Selection (Filtered by State)
# -------------------------------------------------
st.subheader("🏙 City‑Level Drill‑Down")

cities = sorted(state_df["City"].dropna().unique())

selected_city = st.selectbox(
    "Select City",
    cities
)

city_df = state_df[state_df["City"] == selected_city]

# -------------------------------------------------
# City‑Level KPIs
# -------------------------------------------------
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

# -------------------------------------------------
# Price per Sqft by Locality (Chart)
# -------------------------------------------------
st.subheader(f"📈 {selected_city} – Avg Price per Sqft by Locality")

price_chart = (
    city_df.groupby("Locality")["Price_per_Sqft"]
    .mean()
    .sort_values(ascending=False)
)

st.bar_chart(price_chart)

# -------------------------------------------------
# Locality‑Level Table
# -------------------------------------------------
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

# -------------------------------------------------
# Footer
# -------------------------------------------------
st.markdown("---")
st.caption("✅ Person‑2 | State‑Level Detail View | Streamlit Dashboard")
