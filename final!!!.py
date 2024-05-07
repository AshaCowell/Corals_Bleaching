#Import necessary modules
import pandas as pd
import zipfile
import geopandas as gpd
import folium
from folium.plugins import HeatMap

# Load the dataset
file_path = "/content/CoralBleaching-2.xlsx"
coral_data = pd.read_excel(file_path)

# Display the first few rows of the DataFrame
print(coral_data.head())

# Summary statistics
print(coral_data.describe())

# Information about the DataFrame
print(coral_data.info())

# Calculate summary statistics
summary_stats = coral_data_cleaned.describe()
print("Summary Statistics:")
print(summary_stats)

# Correlation analysis
# Drop non-numeric columns before correlation analysis
coral_data_numeric = coral_data_cleaned.select_dtypes(include=['number'])
correlation_matrix = coral_data_numeric.corr()
print("Correlation Matrix:")
print(correlation_matrix)

# Time series plot of bleaching events over the years
plt.figure(figsize=(10, 6))
sns.countplot(x='YEAR', data=coral_data_cleaned, palette='viridis')
plt.title('Bleaching Events Over the Years')
plt.xlabel('Year')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.show()

# Check for missing values in each column
missing_values = coral_data.isnull().sum()

# Display columns with missing values
print("Columns with missing values:")
print(missing_values[missing_values > 0])

# Selecting relevant columns
relevant_columns = ['REGION', 'SUBREGION', 'LOCATION', 'SEVERITY_CODE','BLEACHING_SEVERITY','LAT', 'LON', 'YEAR']
coral_subset = coral_data[relevant_columns]

# Dropping rows with missing values
coral_subset_cleaned = coral_subset.dropna(subset=relevant_columns)

# Displaying the first few rows of the cleaned DataFrame
print(coral_subset_cleaned.head())

# Saving the cleaned DataFrame to a new file
cleaned_file_path = "/content/CoralBleaching_Cleaned.xlsx"
coral_subset_cleaned.to_excel(cleaned_file_path, index=False)

# Check the column names in the DataFrame
print(coral_subset_cleaned.columns)

# Selecting relevant columns
relevant_columns = ['REGION', 'SUBREGION', 'LOCATION', 'BLEACHING_SEVERITY', 'SEVERITY_CODE', 'LAT', 'LON', 'YEAR']

# Extracting the relevant subset of data
coral_subset = coral_data[relevant_columns]

# Dropping rows with missing values
coral_subset_cleaned = coral_subset.dropna(subset=relevant_columns)

# Displaying the first few rows of the cleaned DataFrame
print(coral_subset_cleaned.head())

# Saving the cleaned DataFrame to a new Excel file
cleaned_file_path = "/content/CoralBleaching_Cleaned.xlsx"
coral_subset_cleaned.to_excel(cleaned_file_path, index=False)

# Check the column names in the DataFrame
print(coral_subset_cleaned.columns)

# Create a map centered around the mean latitude and longitude
coral_map = folium.Map(location=[coral_subset_cleaned['LAT'].mean(), coral_subset_cleaned['LON'].mean()], zoom_start=4)

# Add markers for each bleaching event with severity as popup
for index, row in coral_subset_cleaned.iterrows():
    folium.Marker([row['LAT'], row['LON']], popup=row['BLEACHING_SEVERITY']).add_to(coral_map)

coral_map.save('coral_bleaching_map.html')

from folium.plugins import HeatMap

# Create a map centered around the mean latitude and longitude
coral_heatmap = folium.Map(location=[coral_subset_cleaned['LAT'].mean(), coral_subset_cleaned['LON'].mean()], zoom_start=4)

# Convert severity codes to numeric values for heatmap intensity
coral_subset_cleaned.loc[:, 'SEVERITY_CODE'] = pd.to_numeric(coral_subset_cleaned['SEVERITY_CODE'])


# Create a HeatMap layer
heat_data = [[row['LAT'], row['LON'], row['SEVERITY_CODE']] for index, row in coral_subset_cleaned.iterrows()]
HeatMap(heat_data).add_to(coral_heatmap)

# Save the heatmap as an HTML file
coral_heatmap.save('coral_bleaching_heatmap.html')

# Filter out 'Unknown' and 'No Bleaching', and keep only 'High', 'Medium', and 'Low' severity levels
severity_over_time_filtered = coral_subset_cleaned[coral_subset_cleaned['BLEACHING_SEVERITY'].isin(['HIGH', 'Medium', 'Low'])]

# Group the data by year and severity level and count the occurrences
severity_over_time = severity_over_time_filtered.groupby(['YEAR', 'BLEACHING_SEVERITY']).size().reset_index(name='COUNT')

# Plotting the severity over time
plt.figure(figsize=(12, 6))
sns.lineplot(data=severity_over_time, x='YEAR', y='COUNT', hue='BLEACHING_SEVERITY', marker='o')
plt.title('Severity of Coral Bleaching Over Time (Excluding Unknown and No Bleaching)')
plt.xlabel('Year')
plt.ylabel('Count of Bleaching Events')
plt.legend(title='Severity Level')
plt.grid(True)
plt.show()

# Filter out rows with unknown severity and no bleaching
filtered_coral_subset = coral_subset_cleaned[~coral_subset_cleaned['BLEACHING_SEVERITY'].isin(['Severity Unknown', 'No Bleaching'])]

# Group the filtered data by region and severity, and count the occurrences of each severity level
severity_by_region = filtered_coral_subset.groupby(['REGION', 'BLEACHING_SEVERITY']).size().unstack(fill_value=0)

# Plot the distribution of severity levels for each region as a bar graph
severity_by_region.plot(kind='bar', stacked=True, figsize=(12, 6))
plt.title('Distribution of Bleaching Severity by Region (Excluding Unknown and No Bleaching)')
plt.xlabel('Region')
plt.ylabel('Count')
plt.legend(title='Bleaching Severity')
plt.show()

# Filter the cleaned dataset for Australia and non-'No Bleaching' and non-'Unknown' severity levels
australia_data_filtered = australia_data[~australia_data['BLEACHING_SEVERITY'].isin(['No Bleaching', 'Severity Unknown'])]

# Group the Australia data by year and severity, and count the occurrences of each severity level
severity_by_year_australia_filtered = australia_data_filtered.groupby(['YEAR', 'BLEACHING_SEVERITY']).size().unstack(fill_value=0)

# Plot the distribution of severity levels over time for Australia
severity_by_year_australia_filtered.plot(kind='line', figsize=(12, 6))
plt.title('Evolution of Bleaching Severity Over Time in Australia (Excluding No Bleaching and Unknown)')
plt.xlabel('Year')
plt.ylabel('Count')
plt.legend(title='Bleaching Severity')
plt.show()


# Path to the zip file
zip_file_path = "/content/World_Countries_(Generalized)_-573431906301700955.zip"

# Extract the shapefile
with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    zip_ref.extractall("/content/")

# Load the shapefile for Australia
australia_shapefile_path = "/content/World_Countries_Generalized.shp"
australia_shapefile = gpd.read_file(australia_shapefile_path)

# Display the first few rows of the shapefile
print(australia_shapefile.head())

# Load a shapefile of Australia
australia_shapefile = gpd.read_file('/content/World_Countries_Generalized.shp')

# Filter the data for Australia and group by year and coordinates
australia_data_grouped = coral_subset_cleaned[coral_subset_cleaned['REGION'] == 'Australia'].groupby(['YEAR', 'LAT', 'LON', 'BLEACHING_SEVERITY']).size().reset_index(name='count')

# Create a map centered on Australia
m = folium.Map(location=[-25.2744, 133.7751], zoom_start=4)

# Create a HeatMap layer
heat_data = [[row['LAT'], row['LON'], row['count']] for index, row in australia_data_grouped.iterrows()]
HeatMap(heat_data).add_to(m)

# Display the map
m.save('australia_bleaching_heatmap.html')

# Path to the zip file
zip_file_path = "/content/World_Countries_(Generalized)_-573431906301700955.zip"

# Extract the shapefile
with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    zip_ref.extractall("/content/")

# Load the shapefile for the Americas
americas_shapefile_path = "/content/World_Countries_Generalized.shp"
americas_shapefile = gpd.read_file(americas_shapefile_path)

# Display the first few rows of the shapefile
print(americas_shapefile.head())

# Load a shapefile of the Americas
americas_shapefile = gpd.read_file('/content/World_Countries_Generalized.shp')

# Filter the data for the Americas and group by year and coordinates
americas_data_grouped = coral_subset_cleaned[coral_subset_cleaned['REGION'] == 'Americas'].groupby(['YEAR', 'LAT', 'LON', 'BLEACHING_SEVERITY']).size().reset_index(name='count')

# Create a map centered on the Americas
m = folium.Map(location=[0, -90], zoom_start=2)

# Create a HeatMap layer
heat_data = [[row['LAT'], row['LON'], row['count']] for index, row in americas_data_grouped.iterrows()]
HeatMap(heat_data).add_to(m)

# Display the map
m.save('americas_bleaching_heatmap.html')

# Filter the cleaned dataset for the Americas and non-'No Bleaching' and non-'Unknown' severity levels
americas_data_filtered = coral_subset_cleaned[(coral_subset_cleaned['REGION'] == 'Americas') &
                                               (~coral_subset_cleaned['BLEACHING_SEVERITY'].isin(['No Bleaching', 'Severity Unknown']))]

# Group the Americas data by year and severity, and count the occurrences of each severity level
severity_by_year_americas_filtered = americas_data_filtered.groupby(['YEAR', 'BLEACHING_SEVERITY']).size().unstack(fill_value=0)

# Plot the distribution of severity levels over time for the Americas
severity_by_year_americas_filtered.plot(kind='line', figsize=(12, 6))
plt.title('Evolution of Bleaching Severity Over Time in the Americas (Excluding No Bleaching and Unknown)')
plt.xlabel('Year')
plt.ylabel('Count')
plt.legend(title='Bleaching Severity')
plt.show()