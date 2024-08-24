import pandas as pd
import streamlit as st

# Introduction: This application allows users to filter and view hurricane data, with options to visualize hurricane paths on a map.
# Dependencies: pandas, streamlit

# Load and clean the hurricane data
file_path = 'C:\\Users\\jhnnk\\Documents\\Python312\\Hurricane_Data.csv'  # Update this to your file path
hurricane_data = pd.read_csv(file_path, skiprows=2)

# Rename the columns for clarity
hurricane_data.columns = [
    'Rank', '#', 'Date', 'Time', 'Latitude', 'Longitude', 'Max Winds (kt)',
    'SS', 'RMW (nm)', 'Central Pressure (mb)', 'States Affected', 'Name'
]

# Convert the 'Date' column to datetime format to extract the year
hurricane_data['Date'] = pd.to_datetime(hurricane_data['Date'], errors='coerce')
hurricane_data['Year'] = hurricane_data['Date'].dt.year

# Ensure Latitude and Longitude are numeric
hurricane_data['Latitude'] = pd.to_numeric(hurricane_data['Latitude'], errors='coerce')
hurricane_data['Longitude'] = pd.to_numeric(hurricane_data['Longitude'], errors='coerce')

# Clean the data by removing rows with missing Name values
hurricane_data_cleaned = hurricane_data.dropna(subset=['Name'])

# Streamlit application title
st.title("Hurricane Data Viewer with Filters")

# Sidebar Filters
st.sidebar.header("Filter Options")

# Year filter
year_options = hurricane_data_cleaned['Year'].dropna().unique()
selected_year = st.sidebar.multiselect("Select Year(s):", year_options, default=year_options)

# Saffir-Simpson category filter
ss_options = hurricane_data_cleaned['SS'].dropna().unique()
selected_ss = st.sidebar.multiselect("Select Saffir-Simpson Category:", ss_options, default=ss_options)

# Maximum wind speed filter
min_wind = int(hurricane_data_cleaned['Max Winds (kt)'].min())
max_wind = int(hurricane_data_cleaned['Max Winds (kt)'].max())
selected_wind = st.sidebar.slider("Select Maximum Wind Speed (kt):", min_wind, max_wind, (min_wind, max_wind))

# Filter the data based on user selection
filtered_data = hurricane_data_cleaned[
    (hurricane_data_cleaned['Year'].isin(selected_year)) &
    (hurricane_data_cleaned['SS'].isin(selected_ss)) &
    (hurricane_data_cleaned['Max Winds (kt)'] >= selected_wind[0]) &
    (hurricane_data_cleaned['Max Winds (kt)'] <= selected_wind[1])
]

# User selects a hurricane by name
selected_hurricane = st.selectbox("Select a Hurricane:", filtered_data['Name'].unique())

# Display the data for the selected hurricane
hurricane_info = filtered_data[filtered_data['Name'] == selected_hurricane]

st.subheader(f"Details for Hurricane {selected_hurricane}")
st.write(hurricane_info)

# Visualize the hurricane path on a map (if latitude and longitude data are available)
if not hurricane_info[['Latitude', 'Longitude']].isnull().values.any():
    # Rename the columns to 'lat' and 'lon' for Streamlit compatibility
    hurricane_info = hurricane_info.rename(columns={'Latitude': 'lat', 'Longitude': 'lon'})

    # Ensure all latitude and longitude values are valid (e.g., within possible ranges)
    hurricane_info = hurricane_info[(hurricane_info['lat'].between(-90, 90)) & (hurricane_info['lon'].between(-180, 180))]

    if not hurricane_info.empty:
        st.map(hurricane_info[['lat', 'lon']])
    else:
        st.warning("No valid coordinates available for mapping.")
else:
    st.warning("Latitude and Longitude data are missing or invalid.")
