import json

def generate_schema(data):
    if isinstance(data, list):
        data = data[0]

    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": {},
    }

    for key, value in data.items():
        if isinstance(value, dict):
            schema["properties"][key] = generate_schema(value)
        else:
            schema["properties"][key] = {"type": type(value).__name__}

    return schema

json_file = 'testmo-export-grubtech-shorter.json'
with open(json_file, 'r') as f:
    data = json.load(f)
schema = generate_schema(data)

output_file = 'output_schema.json'
with open(output_file, 'w') as f:
    json.dump(schema, f, indent=4)