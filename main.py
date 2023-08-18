import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# Load data
districts_data = pd.read_csv("dataset/BostonPoliceDistricts.csv")
crime_data = pd.read_csv("dataset/BostonCrime2021_7000_sample.csv")


# Set a custom page title and favicon
st.set_page_config(page_title="🕵️‍♂️ Boston Crime Insights", page_icon="🔍")

# Create a dictionary to map district codes to district names
district_mapping = dict(zip(districts_data["District"], districts_data["District Name"]))

# Streamlit UI setup
# st.image("crime_banner.jpg", use_column_width=True)  # Crime scene banner
st.title("Unmasking Boston's Secrets 🕶️")
st.markdown("Welcome, detective! It's time to dive into the world of Boston's crime data. As you explore, remember: **every data point tells a story**. 📜")
st.sidebar.title("Filters")

# Display district dropdown in the sidebar
selected_district = st.sidebar.selectbox("Select District", districts_data["District Name"].tolist())

# Get the district code based on selected district name
selected_district_code = districts_data[districts_data["District Name"] == selected_district]["District"].iloc[0]

# Filter crime data based on selected district code
filtered_crime_data = crime_data[crime_data["DISTRICT"] == selected_district_code].copy()

# Rename columns to match expected names
filtered_crime_data.rename(columns={"Lat": "latitude", "Long": "longitude"}, inplace=True)

# Display a mysterious magnifying glass image
# st.image("magnifying_glass.png", use_column_width=True)

# Display crime data sample
st.write("### Clues Gathered So Far 🧐")
st.write(filtered_crime_data)

# Add a suspenseful quote
st.markdown("> \"The city never sleeps, and neither do its secrets.\" - Unknown")

# Simple chart example: Offense Code Group distribution
offense_group_counts = filtered_crime_data["OFFENSE_CODE_GROUP"].value_counts()

# Map example
st.write("### Crime Location Map")
st.map(filtered_crime_data)


# Filter out rows with missing or empty offense code group values
offense_group_counts = offense_group_counts[offense_group_counts.index != ""]
if not offense_group_counts.empty:
    st.write("### Offense Code Group Distribution")
    plt.bar(offense_group_counts.index, offense_group_counts.values)
    plt.xticks(rotation=90)
    st.pyplot(plt)
else:
    st.write("No valid offense code group data available for the selected district.")

# Show more details about a specific incident
selected_incident = st.selectbox("Select Incident", filtered_crime_data["INCIDENT_NUMBER"].tolist())
selected_incident_data = filtered_crime_data[filtered_crime_data["INCIDENT_NUMBER"] == selected_incident]
st.write("### Selected Incident Details")
st.write(selected_incident_data)

# Add more features, charts, and interactive elements as required by your assignment

# Time-based Analysis for Month
st.sidebar.subheader("Time-based Analysis for Month")
min_month = int(filtered_crime_data["MONTH"].min())
max_month = int(filtered_crime_data["MONTH"].max()) + 1  # Add a small offset

selected_month = st.sidebar.slider("Select Month", min_value=min_month, max_value=max_month)
filtered_month_data = filtered_crime_data[filtered_crime_data["MONTH"] == selected_month]

# Pie Chart for Day of Week
st.write("### Pie Chart of Crimes by Day of Week")
day_of_week_counts = filtered_month_data["DAY_OF_WEEK"].value_counts()
if not day_of_week_counts.empty:
    fig = px.pie(names=day_of_week_counts.index, values=day_of_week_counts.values, 
                 title="Crimes by Day of Week")
    # annotations = [dict(text=f'{label}<br>{value}', x=0.5, y=0.5, font_size=12, showarrow=False) 
    #                for label, value in zip(day_of_week_counts.index, day_of_week_counts.values)]
    # fig.update_layout(annotations=annotations)
    st.plotly_chart(fig)
else:
    st.write("No data available for the selected month.")

# Crime Trends Chart for Month
st.write("### Crime Trends Chart for Month")
crime_counts_by_month = filtered_crime_data["MONTH"].value_counts().sort_index()

# Update the chart dynamically based on the selected month
plt.plot(crime_counts_by_month.index, crime_counts_by_month.values, marker='o')
plt.xlabel("Month")
plt.ylabel("Number of Crimes")
plt.title("Crime Trends by Month")
st.pyplot(plt)

# Footer with a closing statement
st.markdown("🔍 Keep investigating! Remember, the truth is out there. 🌄")
