import streamlit as st
import pandas as pd
import plotly.express as px
import geopandas as gpd
import folium
from streamlit_folium import st_folium

# Load Data
st.title("🌍 India Air Quality Monitor")

uploaded_file = st.file_uploader("Upload Air Quality CSV", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Display Raw Data
    st.write("### 📊 Raw Data Preview")
    st.dataframe(df)

    # Convert Date Column (if necessary)
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"])

    # Select Columns
    pollutant = st.selectbox("Select Pollutant", ["PM2.5", "PM10", "NO2", "SO2", "CO", "O3"])

    # Line Chart for Air Quality Over Time
    st.write(f"### 📈 {pollutant} Levels Over Time")
    fig = px.line(df, x="date", y=pollutant, color="city", title=f"{pollutant} Trends")
    st.plotly_chart(fig)

    # Bar Chart for Pollution Levels in Cities
    st.write(f"### 📊 {pollutant} Levels Across Cities")
    fig_bar = px.bar(df.groupby("city")[pollutant].mean().reset_index(),
                     x="city", y=pollutant, title=f"Avg {pollutant} Levels")
    st.plotly_chart(fig_bar)

    # Interactive Map with Color Gradient
    st.write("### 🗺️ Air Quality Map")
    india_map = gpd.read_file("https://raw.githubusercontent.com/geohacker/india/master/state/india_telengana.geojson")  # India GeoJSON File
    df_avg = df.groupby("state")[pollutant].mean().reset_index()
    df_avg.columns = ["state", "value"]

    india_map = india_map.merge(df_avg, left_on="st_nm", right_on="state", how="left")

    m = folium.Map(location=[20.5937, 78.9629], zoom_start=5)
    folium.Choropleth(
        geo_data=india_map,
        name="choropleth",
        data=india_map,
        columns=["state", "value"],
        key_on="feature.properties.st_nm",
        fill_color="YlOrRd",
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name=f"{pollutant} Levels",
    ).add_to(m)

    st_folium(m, width=700, height=500)
