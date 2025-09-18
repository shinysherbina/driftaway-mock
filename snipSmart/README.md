# snipSmart API Server

This is a lightweight Node.js HTTP server that exposes the `snipSmart` JavaScript utility as a REST API. It is designed to be called by Python MCP tools to clean AI-generated responses before parsing.

## Endpoints

- **POST /clean**: Cleans an AI-generated response.
- **GET /health**: A health check endpoint.

## Setup

1. Navigate to the `snipSmart` directory:
   ```bash
   cd snipSmart
   ```

2. Install the required dependencies:
   ```bash
   npm install
   ```

3. Start the server:
   ```bash
   node server.js
   ```

The server will start on `http://localhost:3000`.

## Example Python Usage

Here is an example of how to call the `/clean` endpoint from a Python script using the `requests` library.

```python
import requests
import json

# The raw response from an AI model
raw_text = '''
Here is the JSON you requested:
```json
{
    "name": "John Doe",
    "age": 30,
    "isStudent": false,
    "courses": [
        {"title": "History", "credits": 3},
        {"title": "Math", "credits": 4}
    ]
}
```
I hope this is helpful!
'''

# The URL of the snipSmart server
url = 'http://localhost:3000/clean'

# The payload to send to the server
payload = {
    'text': raw_text,
    'format': 'json'
}

# Set the headers
headers = {
    'Content-Type': 'application/json'
}

try:
    # Make the POST request
    response = requests.post(url, data=json.dumps(payload), headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        cleaned_data = response.json()
        print("Cleaned data:")
        # The cleaned data is in the 'data' field, which is a string.
        # To use it as a Python dictionary, you need to parse it.
        parsed_json = json.loads(cleaned_data['data'])
        print(json.dumps(parsed_json, indent=2))
    else:
        print(f"Error: {response.status_code}")
        print(response.json())

except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")

```
