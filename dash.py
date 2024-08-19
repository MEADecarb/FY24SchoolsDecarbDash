import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import matplotlib.pyplot as plt
from folium.features import CustomIcon

# Load the dataset from GitHub
csv_url = "https://raw.githubusercontent.com/your-username/FY24SchoolsDecarbDash/main/schools24_geo.csv"
data = pd.read_csv(csv_url)

# Set up the Streamlit app
st.title("Maryland Schools Decarbonization Projects")

# Create a map
st.header("Map of Schools Involved in Decarbonization Projects")
map_center = [data['LAT'].mean(), data['LON'].mean()]
m = folium.Map(location=map_center, zoom_start=8)

for _, row in data.iterrows():
    if row['ENOUGH ACT School '] == 'Yes':
        # Custom icon for Enough Act Schools
        icon = folium.CustomIcon(icon_image="https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-red.png", icon_size=(30, 30))
        folium.Marker(
            location=[row['LAT'], row['LON']],
            popup=f"{row['SCHOOL']} - {row['PROJECT']}",
            tooltip=row['SCHOOL'],
            icon=icon
        ).add_to(m)
    else:
        # Default marker for other schools
        folium.Marker(
            location=[row['LAT'], row['LON']],
            popup=f"{row['SCHOOL']} - {row['PROJECT']}",
            tooltip=row['SCHOOL']
        ).add_to(m)

# Display the map
st_folium(m, width=700, height=500)

# Create a bar chart of total award amounts by project type
st.header("Total Award Amounts by Project Type")
data['AWARD'] = data['AWARD'].replace('[\$,]', '', regex=True).astype(float)
award_by_project = data.groupby('PROJECT')['AWARD'].sum().sort_values(ascending=False)

fig, ax = plt.subplots()
award_by_project.plot(kind='bar', ax=ax)
ax.set_ylabel('Total Award Amount ($)')
ax.set_xlabel('Project Type')
ax.set_title('Total Award Amounts by Project Type')

st.pyplot(fig)
