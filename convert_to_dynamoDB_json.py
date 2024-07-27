import json

def convert_to_dynamodb_json(data):
    if isinstance(data, dict):
        dynamodb_data = {"M": {k: convert_to_dynamodb_json(v) for k, v in data.items()}}
    elif isinstance(data, list):
        dynamodb_data = {"L": [convert_to_dynamodb_json(v) for v in data]}
    elif isinstance(data, str):
        dynamodb_data = {"S": data}
    elif isinstance(data, (int, float)):
        dynamodb_data = {"N": str(data)}
    elif isinstance(data, bool):
        dynamodb_data = {"BOOL": data}
    elif data is None:
        dynamodb_data = {"NULL": True}
    else:
        raise TypeError("Unsupported data type: {}".format(type(data)))
    return dynamodb_data

with open('/mnt/data/random_geojson_data.json') as f:
    original_data = json.load(f)

dynamodb_data = convert_to_dynamodb_json(original_data)

with open('/mnt/data/dynamodb_formatted_data.json', 'w') as f:
    json.dump(dynamodb_data, f, indent=2)
