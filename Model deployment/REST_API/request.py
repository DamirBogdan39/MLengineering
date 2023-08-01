"""
This script showcases the usage of the api to get the prediction.
"""

# Dependencies
import requests
import json

# Function to load json 
def load_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
    except json.JSONDecodeError:
        print(f"Invalid JSON format in file: {file_path}")
        return None
    
# Define the API endpoint URL
url = "http://localhost:8000/predict/"

# Send the POST request with JSON data to the server
response = requests.post(url, json=load_json_file('sample.json'))

# Check if the request was successful (status code 200)
if response.status_code == 200:
    result = response.json()
    print("Predictions:", result["predictions"])
else:
    print(f"Error: {response.status_code} - {response.text}")
