import pandas as pd
import zipfile
import geopandas as gpd
import folium
from folium.plugins import HeatMap
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
coral_data = pd.read_excel('CoralBleaching-2.xlsx')

# Data Cleaning
coral_data_cleaned = coral_data.dropna(subset=['REGION', 'SUBREGION', 'LOCATION', 'SEVERITY_CODE','BLEACHING_SEVERITY','LAT', 'LON', 'YEAR'])

# Summary Statistics
summary_stats = coral_data_cleaned.describe()

# Correlation Analysis
coral_data_numeric = coral_data_cleaned.select_dtypes(include=['number'])
correlation_matrix = coral_data_numeric.corr()

# Bleaching Events Over the Years
plt.figure(figsize=(10, 6))
sns.countplot(x='YEAR', data=coral_data_cleaned, palette='viridis')
plt.title('Bleaching Events Over the Years')
plt.xlabel('Year')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.show()

# Heatmap and Map Generation
heat_data = [[row['LAT'], row['LON'], row['SEVERITY_CODE']] for index, row in coral_data_cleaned.iterrows()]

coral_heatmap = folium.Map(location=[coral_data_cleaned['LAT'].mean(), coral_data_cleaned['LON'].mean()], zoom_start=4)
HeatMap(heat_data).add_to(coral_heatmap)
coral_heatmap.save('coral_bleaching_heatmap.html')

coral_map = folium.Map(location=[coral_data_cleaned['LAT'].mean(), coral_data_cleaned['LON'].mean()], zoom_start=4)
for index, row in coral_data_cleaned.iterrows():
    folium.Marker([row['LAT'], row['LON']], popup=row['BLEACHING_SEVERITY']).add_to(coral_map)
coral_map.save('coral_bleaching_map.html')

# Visualization of Bleaching Severity Over Time
severity_over_time_filtered = coral_data_cleaned[coral_data_cleaned['BLEACHING_SEVERITY'].isin(['HIGH', 'Medium', 'Low'])]
severity_over_time = severity_over_time_filtered.groupby(['YEAR', 'BLEACHING_SEVERITY']).size().reset_index(name='COUNT')

plt.figure(figsize=(12, 6))
sns.lineplot(data=severity_over_time, x='YEAR', y='COUNT', hue='BLEACHING_SEVERITY', marker='o')
plt.title('Severity of Coral Bleaching Over Time (Excluding Unknown and No Bleaching)')
plt.xlabel('Year')
plt.ylabel('Count of Bleaching Events')
plt.legend(title='Severity Level')
plt.grid(True)
plt.show()

# Regional Analysis
filtered_coral_subset = coral_data_cleaned[~coral_data_cleaned['BLEACHING_SEVERITY'].isin(['Severity Unknown', 'No Bleaching'])]
severity_by_region = filtered_coral_subset.groupby(['REGION', 'BLEACHING_SEVERITY']).size().unstack(fill_value=0)

severity_by_region.plot(kind='bar', stacked=True, figsize=(12, 6))
plt.title('Distribution of Bleaching Severity by Region (Excluding Unknown and No Bleaching)')
plt.xlabel('Region')
plt.ylabel('Count')
plt.legend(title='Bleaching Severity')
plt.show()

# Bleaching Severity Over Time in Australia
australia_data_filtered = coral_data_cleaned[(coral_data_cleaned['REGION'] == 'Australia') &
                                             (~coral_data_cleaned['BLEACHING_SEVERITY'].isin(['No Bleaching', 'Severity Unknown']))]
severity_by_year_australia_filtered = australia_data_filtered.groupby(['YEAR', 'BLEACHING_SEVERITY']).size().unstack(fill_value=0)

severity_by_year_australia_filtered.plot(kind='line', figsize=(12, 6))
plt.title('Evolution of Bleaching Severity Over Time in Australia (Excluding No Bleaching and Unknown)')
plt.xlabel('Year')
plt.ylabel('Count')
plt.legend(title='Bleaching Severity')
plt.show()

# Extract shapefiles and create maps for Australia and Americas
with zipfile.ZipFile("World_Countries_(Generalized)_-573431906301700955.zip", 'r') as zip_ref:
    zip_ref.extractall("extracted_files/")

australia_shapefile = gpd.read_file("extracted_files/World_Countries_Generalized.shp")
americas_shapefile = gpd.read_file("extracted_files/World_Countries_Generalized.shp")

# Map Generation for Australia
australia_data_grouped = coral_data_cleaned[coral_data_cleaned['REGION'] == 'Australia'].groupby(['YEAR', 'LAT', 'LON', 'BLEACHING_SEVERITY']).size().reset_index(name='count')

m = folium.Map(location=[-25.2744, 133.7751], zoom_start=4)
heat_data = [[row['LAT'], row['LON'], row['count']] for index, row in australia_data_grouped.iterrows()]
HeatMap(heat_data).add_to(m)
m.save('australia_bleaching_heatmap.html')

# Map Generation for Americas
americas_data_grouped = coral_data_cleaned[coral_data_cleaned['REGION'] == 'Americas'].groupby(['YEAR', 'LAT', 'LON', 'BLEACHING_SEVERITY']).size().reset_index(name='count')

m = folium.Map(location=[0, -90], zoom_start=2)
heat_data = [[row['LAT'], row['LON'], row['count']] for index, row in americas_data_grouped.iterrows()]
HeatMap(heat_data).add_to(m)
m.save('americas_bleaching_heatmap.html')

# Severity Over Time in Americas
americas_data_filtered = coral_data_cleaned[(coral_data_cleaned['REGION'] == 'Americas') &
                                            (~coral_data_cleaned['BLEACHING_SEVERITY'].isin(['No Bleaching', 'Severity Unknown']))]
severity_by_year_americas_filtered = americas_data_filtered.groupby(['YEAR', 'BLEACHING_SEVERITY']).size().unstack(fill_value=0)

severity_by_year_americas_filtered.plot(kind='line', figsize=(12, 6))
plt.title('Evolution of Bleaching Severity Over Time in the Americas (Excluding No Bleaching and Unknown)')
plt.xlabel('Year')
plt.ylabel('Count')
plt.legend(title='Bleaching Severity')
plt.show()
