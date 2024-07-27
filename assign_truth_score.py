pip install geopy

import json
import random
from datetime import datetime
from geopy.distance import great_circle

# Load the GeoJSON data from a file
with open('random_geojson_data.json', 'r') as f:
    geojson_data = json.load(f)

# Current time for comparison
current_time = datetime.now()

# Helper function to calculate the distance between two points
def calculate_distance(point1, point2):
    return great_circle(point1, point2).kilometers

# Helper function to calculate the time difference in hours
def time_difference(timestamp):
    report_time = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
    return (current_time - report_time).total_seconds() / 3600

# Calculate the truthScore for each feature
def calculate_truth_score(feature, all_features):
    properties = feature['properties']
    coordinates = feature['geometry']['coordinates']
    
    # Initialize score
    score = 0
    
    # 1. Score improvement for same reportType from multiple unique users
    same_type_reports = [f for f in all_features if f['properties']['reportType'] == properties['reportType']]
    unique_users = set(f['properties']['reportedBy'] for f in same_type_reports)
    user_count = len(unique_users)
    score += min(user_count * 10, 30)  # Cap score at 30
    
    # 2. Score improvement for lower user speed
    if properties['currentSpeed_kmh'] < 50:
        score += 20
    elif properties['currentSpeed_kmh'] < 100:
        score += 10
    
    # 3. Score improvement for matching visibility index and ambient light
    if properties['ambientLight'] < 5000:
        score += 10 if properties['ambientLight'] == 0 else 5
    
    # 4. Score improvement for more recent timestamps
    time_diff = time_difference(properties['timestamp'])
    if time_diff < 1:
        score += 20
    elif time_diff < 5:
        score += 10
    
    # 5. Score improvement for presence of BPM data
    if properties['wearableDeviceBPM'] > 0:
        score += 10
    
    # Ensure the score is between 1 and 100
    return min(max(score, 1), 100)

# Process each feature and assign a truthScore
for feature in geojson_data['features']:
    feature['properties']['truthScore'] = calculate_truth_score(feature, geojson_data['features'])

# Save the updated GeoJSON data to a new file
with open('scored_geojson_data.json', 'w') as f:
    json.dump(geojson_data, f, indent=2)

print("GeoJSON data with truth scores has been generated and saved to 'scored_geojson_data.json'.")
