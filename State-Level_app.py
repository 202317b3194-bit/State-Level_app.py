import streamlit as st
import pandas as pd

# -------------------------------------------------
# Page Configuration
# -------------------------------------------------
st.set_page_config(
    page_title="State-Level Real Estate Insights",
    layout="wide"
)

# -------------------------------------------------
# Load and Prepare Data
# -------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("City_level_data.csv")
    df.columns = df.columns.str.strip()

    # City → State mapping
    city_state_map = {
        "Hyderabad": "Telangana",
        "Vijayawada": "Andhra Pradesh",
        "Chennai": "Tamil Nadu",
        "Madurai": "Tamil Nadu",
        "Mumbai": "Maharashtra",
        "Bengaluru": "Karnataka",
        "New Delhi": "Delhi (NCR)",
        "Gurugram": "Haryana",
        "Kolkata": "West Bengal",
        "Patna": "Bihar",
        "Jaipur": "Rajasthan",
        "Ahmedabad": "Gujarat",
        "Kochi": "Kerala",
        "Puducherry": "Puducherry (UT)",
        "Panaji": "Goa",
        "Shimla": "Himachal Pradesh",
        "Srinagar": "Jammu & Kashmir",
        "Dehradun": "Uttarakhand",
        "Lucknow": "Uttar Pradesh",
        "Raipur": "Chhattisgarh",
        "Bhubaneswar": "Odisha",
        "Ranchi": "Jharkhand",
        "Port Blair": "Andaman & Nicobar",
        "Gangtok": "Sikkim",
        "Aizawl": "Mizoram",
        "Itanagar": "Arunachal Pradesh",
        "Shillong": "Meghalaya",
        "Agartala": "Tripura",
        "Kohima": "Nagaland",
        "Imphal": "Manipur",
        "Dispur": "Assam",
        "Indore": "Madhya Pradesh",
        "Amritsar": "Punjab",
        "Chandigarh": "Chandigarh (UT)",
        "Ladakh": "Ladakh (UT)",
        "Lakshadweep": "Lakshadweep (UT)"
    }

    df["State"] = df["City"].map(city_state_map)

    # Rename columns
    df = df.rename(columns={
        "Bedrooms (BHK)": "BHK",
        "Built-up Area (sqft)": "Area_sqft",
        "Price per Sqft (INR)S": "Price_per_Sqft",
        "Rental Yield (%)": "Rental_Yield",
        "Estimated Sale Price (INR)": "House_Price_Lakh"
    })

    # Clean currency columns
    df["Price_per_Sqft"] = (
        df["Price_per_Sqft"]
        .str.replace("₹", "", regex=False)
        .str.replace(",", "", regex=False)
        .astype(float)
    )

    df["House_Price_Lakh"] = (
        df["House_Price_Lakh"]
        .str.replace("₹", "", regex=False)
        .str.replace(",", "", regex=False)
        .astype(float)
        / 100000
    )

    return df


df = load_data()

# -------------------------------------------------
# App Title
# -------------------------------------------------
st.title("🏠 State‑Level Real Estate Insights")
st.caption("State → City drill‑down view")

# -------------------------------------------------
# State Selection
# -------------------------------------------------
states = sorted(df["State"].dropna().unique())
selected_state = st.selectbox("Select State", states)

state_df = df[df["State"] == selected_state]

# -------------------------------------------------
# State KPIs
# -------------------------------------------------
st.subheader(f"📊 {selected_state} – Key Metrics")

k1, k2, k3, k4 = st.columns(4)

k1.metric("Avg Price / Sqft", f"₹ {state_df['Price_per_Sqft'].mean():,.0f}")
k2.metric("Avg House Price", f"₹ {state_df['House_Price_Lakh'].mean():.2f} L")
k3.metric("Avg Rental Yield", f"{state_df['Rental_Yield'].mean():.2f}%")
k4.metric("Total Listings", len(state_df))

# -------------------------------------------------
# City Selection
# -------------------------------------------------
st.subheader("🏙 City‑Level Drill‑Down")

cities = sorted(state_df["City"].unique())
selected_city = st.selectbox("Select City", cities)

city_df = state_df[state_df["City"] == selected_city]

# -------------------------------------------------
# City KPIs
# -------------------------------------------------
c1, c2, c3 = st.columns(3)

c1.metric("Listings", len(city_df))
c2.metric("Avg Price / Sqft", f"₹ {city_df['Price_per_Sqft'].mean():,.0f}")
c3.metric("Avg BHK", f"{city_df['BHK'].mean():.1f}")

# -------------------------------------------------
# Chart
# -------------------------------------------------
st.subheader(f"📈 {selected_city} – Avg Price per Sqft by Locality")

chart_data = (
    city_df.groupby("Locality")["Price_per_Sqft"]
    .mean()
    .sort_values(ascending=False)
)

st.bar_chart(chart_data)

# -------------------------------------------------
# Table
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
st.caption("State-Level Real Estate Dashboard | Streamlit")
