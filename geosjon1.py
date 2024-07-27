pip install geopy
import random
import json
from datetime import datetime, timedelta
from geopy.distance import great_circle

# Helper function to generate random timestamp
def random_timestamp(start_date, end_date):
    start_timestamp = datetime.timestamp(start_date)
    end_timestamp = datetime.timestamp(end_date)
    random_timestamp = random.uniform(start_timestamp, end_timestamp)
    return datetime.fromtimestamp(random_timestamp).isoformat()

# Helper function to generate random coordinates within Alberta with a focus on Jasper
def random_coordinates():
    # Jasper coordinates and range
    jasper_coords = (53.9333, -118.5844)
    # Define a bounding box around Jasper
    latitude_range = (53.8, 54.0)
    longitude_range = (-118.7, -118.5)
    if random.random() < 0.8:  # 80% chance to be in Jasper area
        return (
            random.uniform(latitude_range[0], latitude_range[1]),
            random.uniform(longitude_range[0], longitude_range[1])
        )
    else:  # 20% chance to be elsewhere in Alberta
        return (
            random.uniform(48.0, 60.0),
            random.uniform(-120.0, -110.0)
        )

# Generate GeoJSON features
def generate_features(num_features):
    report_types = [
        "Wildfire Zones",
        "Shelter",
        "No Gas Present",
        "First Responder zones",
        "Object Blockage",
        "Car Crash Blockage",
        "Slow Area",
        "Low Visibility",
        "Safe Zones"
    ]
    
    start_date = datetime(2024, 7, 26)
    end_date = datetime(2024, 7, 28)

    features = []

    for _ in range(num_features):
        feature = {
            "type": "Feature",
            "properties": {
                "reportType": random.choice(report_types),
                "timestamp": random_timestamp(start_date, end_date),
                "reportedBy": f"user{random.randint(1, 5000)}",
                "currentSpeed_kmh": random.uniform(0, 150),
                "ambientLight": random.uniform(0, 30000),
                "wearableDeviceBPM": random.randint(0, 200)
            },
            "geometry": {
                "type": "Point",
                "coordinates": random_coordinates()
            }
        }
        features.append(feature)

    return {
        "type": "FeatureCollection",
        "features": features
    }

# Create the GeoJSON data
geojson_data = generate_features(10000)

# Save to a file
with open('random_geojson_data.json', 'w') as f:
    json.dump(geojson_data, f, indent=2)

print("GeoJSON data has been generated and saved to 'random_geojson_data.json'.")
