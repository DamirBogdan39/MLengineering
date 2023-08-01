# A script that sends the data to the API and return the prediction to the terminal.

# Load the JSON data from sample.json into the variable DATA
data=$(cat sample.json)

# Run the cURL command to send the POST request
curl -X 'POST' \
  'http://127.0.0.1:8000/predict/' \
  -H 'Content-Type: application/json' \
  -d "$data"