import requests
import json
from datetime import datetime

# URL of the API endpoint
#url = "https://api.example.com/data"
path = "https://www.porssisahkoa.fi/api/Prices/GetPrices?mode="
mode = 1
url = f"{path}{mode}"
print (url)

API_CALL = False

if API_CALL:
    # Making a GET request to the API
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the response JSON data
        data = response.json()
        print(data)
    else:
        print("Failed to fetch data:", response.status_code)


# JSON string
json_string = '''
[
    {"name": "Alice", "age": 30, "city": "New York"},
    {"name": "Bob", "age": 25, "city": "Los Angeles"},
    {"name": "Charlie", "age": 35, "city": "Chicago"}
]
'''

# Parsing the JSON string into a Python object
data = json.loads(json_string)

# Now `data` is a Python list of dictionaries
for person in data:
    print(f"Name: {person['name']}, Age: {person['age']}, City: {person['city']}")



elering_data = {
    "fi": [
      {
        "timestamp": 1712005200,
        "price": 0.33
      },
      {
        "timestamp": 1712008800,
        "price": 5.54
      },
      {
        "timestamp": 1712012400,
        "price": 1.28
      },
      {
        "timestamp": 1712016000,
        "price": 0.6
      },
      {
        "timestamp": 1712019600,
        "price": 0.84
      },
      {
        "timestamp": 1712023200,
        "price": 1.51
      },
      {
        "timestamp": 1712026800,
        "price": 7.01
      },
      {
        "timestamp": 1712030400,
        "price": 39.89
      },
      {
        "timestamp": 1712034000,
        "price": 50.89
      },
      {
        "timestamp": 1712037600,
        "price": 56.05
      },
      {
        "timestamp": 1712041200,
        "price": 46.82
      },
      {
        "timestamp": 1712044800,
        "price": 38.29
      },
      {
        "timestamp": 1712048400,
        "price": 39.3
      },
      {
        "timestamp": 1712052000,
        "price": 39.28
      },
      {
        "timestamp": 1712055600,
        "price": 38.37
      },
      {
        "timestamp": 1712059200,
        "price": 33.38
      },
      {
        "timestamp": 1712062800,
        "price": 25.1
      },
      {
        "timestamp": 1712066400,
        "price": 8.83
      },
      {
        "timestamp": 1712070000,
        "price": 41.2
      },
      {
        "timestamp": 1712073600,
        "price": 48.08
      },
      {
        "timestamp": 1712077200,
        "price": 45.65
      },
      {
        "timestamp": 1712080800,
        "price": 42.9
      },
      {
        "timestamp": 1712084400,
        "price": 39.16
      },
      {
        "timestamp": 1712088000,
        "price": 25.7
      }
    ]}

# Now `data` is a Python list of dictionaries
for ele in elering_data['fi']:
    p1 = ele['price']
    p = p1 * 1.24 / 10
    ts = datetime.fromtimestamp(ele['timestamp'])
    print(f"Name: {ts} {ele['timestamp']}, Price: {ele['price']}; {p}")
