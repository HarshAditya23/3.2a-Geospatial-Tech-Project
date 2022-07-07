import folium
import pandas as pd
import pydeck as pdk
import streamlit as st
import matplotlib.pyplot as plt
from datetime import datetime
from folium.plugins import HeatMap
from streamlit_folium import folium_static

# set page layout
st.set_page_config(
    page_title="Travel Exploration",
    page_icon="🌍")

@st.cache
def load_data():
    """ Load the cleaned data with latitudes, longitudes & timestamps """
    travel_log = pd.read_csv("clean_data.csv")
    travel_log["date"] = pd.to_datetime(travel_log["ts"])
    return travel_log

st.title("🌍 Travels Exploration")

travel_data = load_data()

# Calculate the timerange for the slider
min_ts = datetime.strptime(min(travel_data["ts"]), "%Y-%m-%d %H:%M:%S.%f")
max_ts = datetime.strptime(max(travel_data["ts"]), "%Y-%m-%d %H:%M:%S.%f")

st.sidebar.subheader("Inputs")
min_selection, max_selection = st.sidebar.slider(
    "Timeline", min_value=min_ts, max_value=max_ts, value=[min_ts, max_ts]
)

# Toggles for the feature selection in sidebar
satellite_map = st.sidebar.checkbox("Satellite View")
show_heatmap = st.sidebar.checkbox("Show Heatmap")
show_histograms = st.sidebar.checkbox("Show Histograms")
show_detailed_months = st.sidebar.checkbox("Show Detailed Split per Year")

#developed by
st.sidebar.header('About')
st.sidebar.info('Dashboard developed by HarshAditya Gaur, Vaishnavi Uday Honap & Sarunisha Ramachandran\n\n' + \
    '(c) 2022. Gaur Industries Pvt. Ltd. All rights reserved.\n\n' + \
    'Contact: gaurharsh24@gmail.com')
# Filter Data based on selection
st.write(f"Filtering between {min_selection.date()} & {max_selection.date()}")
travel_data = travel_data[
    (travel_data["date"] >= min_selection) & (travel_data["date"] <= max_selection)]
st.write(f"Data Points: {len(travel_data)}")

# Plot the GPS coordinates on the map
# Set the viewport location
# Render
if satellite_map:
    st.write(pdk.Deck(
            map_style="mapbox://styles/mapbox/satellite-v9",
            layers=[pdk.Layer("ScatterplotLayer",
            travel_data,
            pickable=True,
            opacity=0.5,
            filled=True,
            radius_scale=0.25,
            radius_min_pixels=3,
            radius_max_pixels=5,
            line_width_min_pixels=0.01,
            get_position='[longitude, latitude]',
            get_fill_color=[255, 0, 0],
            get_line_color=[0, 0, 0])],
            initial_view_state={
                    'latitude': 26.26841,
                    'longitude' : 73.00594,
                    'zoom': 12,
                    'bearing': 0,
                    'pitch': 0},
            tooltip={"html": "<b>Latitude: </b> {latitude} <br/>"
                             "<b>Longitude: </b> {longitude} <br/>"}))
else:
    st.write(pdk.Deck(
            map_style="mapbox://styles/mapbox/light-v9",
            layers=[pdk.Layer("ScatterplotLayer",
            travel_data,
            pickable=True,
            opacity=0.5,
            filled=True,
            radius_scale=0.25,
            radius_min_pixels=3,
            radius_max_pixels=5,
            line_width_min_pixels=0.01,
            get_position='[longitude, latitude]',
            get_fill_color=[255, 0, 0],
            get_line_color=[0, 0, 0])],
            initial_view_state={
                    'latitude': 26.26841,
                    'longitude' : 73.00594,
                    'zoom': 12,
                    'bearing': 0,
                    'pitch': 0},
            tooltip={"html": "<b>Latitude: </b> {latitude} <br/>"
                             "<b>Longitude: </b> {longitude} <br/>"}))

if show_heatmap:
    # Plot the heatmap using folium. It is resource intensive!
    # Set the map to center around Jodhpur, Rajasthan
    map_heatmap = folium.Map(location=[26.26841, 73.00594], zoom_start=11)

    # Filter the DF for columns, then remove NaNs
    heat_df = travel_data[["latitude", "longitude"]]
    heat_df = heat_df.dropna(axis=0, subset=["latitude", "longitude"])

    # List comprehension to make list of lists
    heat_data = [
        [row["latitude"], row["longitude"]] for index, row in heat_df.iterrows()]

    # Plot it on the map
    HeatMap(heat_data).add_to(map_heatmap)

    # Display the map using the community component
    st.subheader("Heatmap")
    folium_static(map_heatmap)

if show_histograms:
    # Plot the histograms based on the dates of data points
    years = travel_data.groupby(travel_data["date"].dt.year).count().plot(kind="bar")
    years.set_xlabel("Year of Data Points")
    hist_years = years.get_figure()
    st.subheader("Data Split by Year")
    st.pyplot(hist_years)

    months = travel_data.groupby(travel_data["date"].dt.month).count().plot(kind="bar")
    months.set_xlabel("Month of Data Points")
    hist_months = months.get_figure()
    st.subheader("Data Split by Months")
    st.pyplot(hist_months)

    hours = travel_data.groupby(travel_data["date"].dt.hour).count().plot(kind="bar")
    hours.set_xlabel("Hour of Data Points")
    hist_hours = hours.get_figure()
    st.subheader("Data Split by Hours of Day")
    st.pyplot(hist_hours)

if show_detailed_months:
    month_year = (
        travel_data.groupby([travel_data["date"].dt.year, travel_data["date"].dt.month])
        .count()
        .plot(kind="bar"))
    month_year.set_xlabel("Month, Year of Data Points")
    hist_month_year = month_year.get_figure()
    st.subheader("Data Split by Month, Year")
    st.pyplot(hist_month_year)
