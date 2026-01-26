import requests
from datetime import datetime, timedelta, date
import json

# URL of the API endpoint
path = "https://www.porssisahkoa.fi/api/Prices/GetPrices?mode="
_mode = 1

fortumApi = "https://web.fortum.fi/api/v2/consumption/"
apiParams = "?customerId=3532587&resolution=hour&from=DATE_FROM&to=DATE_TO&latestMeasurement=DATE_LATEST&meteringPointNo=6828369&meteringPointId=643007520004355712&contractType=Electricity&isDistrictHeat=false"
#fortumToken = "41a5c07f-6b91-3960-9636-02dd54050b65"
fortumToken = "eyJ0eXAiOiJKV1QiLCJraWQiOiJMWFdHdnpuWHdneHpTNW9XVTNQcEZGZnlVbEU9IiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiI4ZjExYWFjMi03YzhkLTQ2ZTAtYWIxNC1mOTFkNjVlMmE2ZmMiLCJjdHMiOiJPQVVUSDJfU1RBVEVMRVNTX0dSQU5UIiwiYXV0aF9sZXZlbCI6MCwiYXVkaXRUcmFja2luZ0lkIjoiZjQ0MzAwNDktNGVlMS00MTIxLTg1MmYtOTAwNWMwZWVhYzZhLTQ1MTM5MiIsInN1Ym5hbWUiOiI4ZjExYWFjMi03YzhkLTQ2ZTAtYWIxNC1mOTFkNjVlMmE2ZmMiLCJpc3MiOiJodHRwczovL3Nzby5mb3J0dW0uY29tOjQ0My9hbS9vYXV0aDIiLCJ0b2tlbk5hbWUiOiJhY2Nlc3NfdG9rZW4iLCJ0b2tlbl90eXBlIjoiQmVhcmVyIiwiYXV0aEdyYW50SWQiOiJaOUtkZUE2d0tlUFFUM1pNencxWjR4REVqemsiLCJhdWQiOiJmaW5sYW5kbXlwYWdlc3Byb2QiLCJuYmYiOjE3MTM5MzYzODcsImdyYW50X3R5cGUiOiJhdXRob3JpemF0aW9uX2NvZGUiLCJzY29wZSI6WyJvcGVuaWQiLCJwcm9maWxlIiwicm9sZXMiLCJjcm1kYXRhIl0sImF1dGhfdGltZSI6MTcxMzkzNjM4NywicmVhbG0iOiIvYWxwaGEiLCJleHAiOjE3MTM5Mzk5ODcsImlhdCI6MTcxMzkzNjM4NywiZXhwaXJlc19pbiI6MzYwMCwianRpIjoiS2tHX3lCV2s2US10NlhQWkxUNms4T2VnQlJvIn0.g8gKdXPSTqwTjSSv6RHQusJXiGFF84yNlny1PRlY5Hms-O5SU9fEZQb75hOCqYKlm9YTP6ANdfaZ5f2uu1sivnWupn8yutJA2Vkhzmxe3kQRRuVLGgPPdKsbs5vIyLGwHelFa7hDHoPiTt1FpslsLi6nuPL6LYNpWw0J-cGbLyXsxA8Mq4WMtQaSNk4cThDETsv3oj44XzFnnXOqMapfE6TrwyGoh7v3ANokOwIYHe9hF8mFza7q5GT_WnFMYsTrCqz_xZq15buuvFg8GcsCr7pJ4a0p5Fg1sipShDMBeU58Fc_SzIx1snvAusb0RJbLxmohIPYOlQR8hIPNdRrEBw"

sahkotinApi = "https://sahkotin.fi/prices?fix&vat&start="

datahubApi = "https://oma.datahub.fi/_api/GetConsumptionData"
datahubParams = "?meteringPointEAN=METERINGPOINT&periodStartTS=DATE_FROM&periodEndTS=DATE_TO&unitType=kWh&resolutionDuration=PT1H&productType=8716867000030&settlementRelevant=false&readingType=BN01"
datahubToken = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiIyMjA0NzUtMTIzUiIsIm1haW5Vc2VySWQiOiIyMjA0NzUtMTIzUiIsInVzZXJTZXNzaW9uIjoiX2ExYzQ2MDdkZDY1NGFjZGQwYjVjY2M2OTA3MDlmODdhIiwibmFtZUlEIjoiQUFkelpXTnlaWFF4dzdrZEtyckk3TWoxb3lXOGJJK3hpMzREVHh4QXQ0a3NHQWxwb3BETVZ0UGE3T3dPczlKbVZNc0NOODRTYVpDZkZJYlVqc25QZVhMd2pPOGF2MEpUWXZyaFpoL1RSKzFreGNiOVVKT0dLcEd0WjZoSEwzZ2dWbjJqWXd2bWZIaTcyMEY5YkVwT1ZZN1dUUFBVT3BBaHJ3PT0iLCJuYW1lSURGb3JtYXQiOiJ1cm46b2FzaXM6bmFtZXM6dGM6U0FNTDoyLjA6bmFtZWlkLWZvcm1hdDp0cmFuc2llbnQiLCJjdXN0b21lcklEIjoiMDJCQTYzNUQ1NzBGQkI2ODVDNjk1N0VDQ0RFMEQ1MEVCMjAzQTkyMjVCMEFDMkM1MzNDNUU0MTk5RDA1Nzg1RCIsInNlc3Npb25JbmZvIjoiOGI1NjVmMDctYWFkNi00Zjc5LWI2MzYtYzFhMzI0ZjNkYWMzIiwiaWF0IjoxNzMxNTY2OTE5LCJleHAiOjE3MzE1OTU3MTl9.uH9YnUstcCWw19aVigf31Bx7vS-249o_QwKxgvSnXKs"
meteringPoint = "643007520004355712"

IS_SUMMER_TIME = True

def enable_debug():
    global debug
    debug = True

def disable_debug():
    global debug
    debug = False

def getData(mode=_mode):
    url = f"{path}{mode}"
    if debug:
        print (url)

    # Making a GET request to the API
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the response JSON data
        data = response.json()
        if debug:
            print(data)
        return data
    else:
        print("Failed to fetch data:", response.status_code)
        return None

# Get consumption data for given number of days using fortum api
def getConsumption(days = 1):
    headers = {
        "Authorization": f"Bearer {fortumToken}"
    }
    yesterday = str(getDate(-1 * days))
    today = str(getDate(0))
    path = f"{fortumApi}{apiParams.replace('DATE_FROM',yesterday).replace('DATE_TO',today).replace('DATE_LATESTO',today)}"
    print (path)

    response = requests.get(path, headers=headers)

    if response.status_code == 200:
        return response.json()
        #print(response.json())
    else:
        print("Failed to fetch data:", response.status_code)
        return None

# Get consumption data for given number of days using datahub api
def getConsumptionDatahub(days = 1, token = None):
    deltaDay = (1 + days) * (-1)
    if debug:
        print (deltaDay)
    then = f"{str(getDate(deltaDay))}" #T22:00:00.000Z"
    now = f"{str(getDate(0))}" #T22:00:00.000Z"
    return getConsumptionHistory(then, now, token)

def getConsumptionHistory(then, now, token = None, method='POST'):
    if not now:
        nowStr = then.split('T')[0]
        now = date.fromisoformat(nowStr) + timedelta(days=7)
        #now = f"{nowDate}T22:00:00.000Z"
        if debug:
            print('now', now)
    headers = {
        "Authorization": f"Bearer {token if token else datahubToken}"
    }

    thenUtc = getMidnightIsoFormat(then)
    nowUtc = getMidnightIsoFormat(now)

    if method == 'GET':
        path = f"{datahubApi}{datahubParams.replace('METERINGPOINT',meteringPoint).replace('DATE_FROM',thenUtc).replace('DATE_TO',nowUtc)}"
        if debug:
            print (path)

        response = requests.get(path, headers=headers)
        if debug:
            print (response)
    else:
        data = {
            "MeteringPointEAN": meteringPoint,
            "PeriodEndTS": nowUtc,
            "PeriodStartTS": thenUtc,
            "ProductType": "8716867000030",
            "ReadingType": "0",
            "ResolutionDuration": "PT1H",
            "SettlementRelevant": False,
            "UnitType": "kWh"
        }

        #response = requests.post(datahubApi, headers=headers, json=data)
        response = readFromJson()
        return response

    if response.status_code == 200:
        #print(response.json())
        return response.json()
    else:
        print("Failed to fetch data:", response.status_code)
        return None

# Get price history data for given number of days using sahkotin api
def getSahkotinData(days = 0):
    deltaDay = (1 + days) * (-1)
    if debug:
        print ('deltaDay', deltaDay)
    date = getDate(deltaDay)
    isodate = getMidnightIsoFormat(date)
    # This API requires millisecond format
    url = f"{sahkotinApi}{isodate.replace(':00Z', ':00.000Z')}"
    # old: _url = f"{sahkotinApi}{date}T22:00:00.000Z"
    if debug:
        print ('url', url)

    # Making a GET request to the API
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the response JSON data
        data = response.json()
        #print(data)
        return data
    else:
        print("Failed to fetch data:", response.status_code)
        return None

# Get price history data for given dates using sahkotin api
def getSahkotinHistory(then, now):
    thenUtc = getMidnightIsoFormat(then)
    
    print ('thenUtc', thenUtc)
    print ('then', then)

    if not now:
        nowUtc = toISOFormat(datetime.fromisoformat(thenUtc) + timedelta(days=3))
        #nowStr = then.split('T')[0]
        #nowDate = date.fromisoformat(nowStr) + timedelta(days=2)
        #now = f"{nowDate}T22:00:00.000Z"
    else:
        nowUtc = getMidnightIsoFormat(now)
    #if debug:
    print ('now', nowUtc)
    print ('now', now)
    url = f"{sahkotinApi}{thenUtc.replace(':00Z', ':00.000Z')}&end={nowUtc.replace(':00Z', ':00.000Z')}"
    print ('url', url)
    #if debug:

    # Making a GET request to the API
    response = requests.get(url)
    if debug:
        print ('response', response)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the response JSON data
        data = response.json()
        #print(data)
        return data
    else:
        print("Failed to fetch data:", response.status_code)
        return None

## Retuens Date object delta days before or after today.
## Return today if delta = 0        
def getDate(delta):
    # Get today's date
    today = datetime.now().date()

    if delta == 0:
        if debug:
            print('today', today)
        return today

    if delta < 0:
        # Calculate yesterday's date by subtracting one day
        yesterday = today - timedelta(days=delta*(-1))
        if debug:
            print('yesterday', yesterday)
        return yesterday

    # Calculate tomorrow's date by adding one day
    tomorrow = today + timedelta(days=delta)
    if debug:
        print('tomorrow', tomorrow)
    return tomorrow

def getMidnightIsoFormat(dateStr):
    # If the string already contains timezone info, extract just the date part
    if isinstance(dateStr, str) and 'T' in dateStr:
        dateStr = dateStr.split('T')[0]
    
    hourDiff = 3 if IS_SUMMER_TIME else 2
    tzinfo = '+03:00' if IS_SUMMER_TIME else '+02:00'
    localtimeStr = f"{dateStr}T00:00:00{tzinfo}"
    localTimeIso = datetime.fromisoformat(localtimeStr)
    utcTime = localTimeIso - timedelta(hours=hourDiff)
    return f"{utcTime}".replace(' ', 'T').replace(tzinfo, 'Z')

def toISOFormat(utcTime):
    dateStr = f"{utcTime}".replace(' ', 'T').split('+')[0]
    return f"{dateStr}Z"

def readFromJson(file='consumption.json'):
    try:
        with open(file, 'r') as file:
            return json.load(file)
    except:
        return None

# Disable debug
disable_debug()
