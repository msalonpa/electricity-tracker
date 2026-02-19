import requests
from datetime import datetime, timedelta, date
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# URL of the API endpoint
path = "https://www.porssisahkoa.fi/api/Prices/GetPrices?mode="
_mode = 1

fortumApi = "https://web.fortum.fi/api/v2/consumption/"
apiParams = "?customerId={customer_id}&resolution=hour&from=DATE_FROM&to=DATE_TO&latestMeasurement=DATE_LATESTO&meteringPointNo={metering_point_no}&meteringPointId={metering_point_id}&contractType=Electricity&isDistrictHeat=false"

# Get sensitive data from environment variables
fortumToken = os.getenv('FORTUM_TOKEN')
fortumCustomerId = os.getenv('FORTUM_CUSTOMER_ID')
fortumMeteringPointNo = os.getenv('FORTUM_METERING_POINT_NO')
fortumMeteringPointId = os.getenv('FORTUM_METERING_POINT_ID')

sahkotinApi = "https://sahkotin.fi/prices?fix&vat&start="

datahubApi = "https://oma.datahub.fi/_api/GetConsumptionData"
datahubParams = "?meteringPointEAN={metering_point_ean}&periodStartTS=DATE_FROM&periodEndTS=DATE_TO&unitType=kWh&resolutionDuration=PT1H&productType=8716867000030&settlementRelevant=false&readingType=BN01"

# Get sensitive data from environment variables
datahubToken = os.getenv('DATAHUB_TOKEN')
meteringPoint = os.getenv('DATAHUB_METERING_POINT_EAN')

IS_SUMMER_TIME = os.getenv('IS_SUMMER_TIME', 'True').lower() == 'true'

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
    if not all([fortumToken, fortumCustomerId, fortumMeteringPointNo, fortumMeteringPointId]):
        print("Error: Missing Fortum API credentials. Please check your environment variables.")
        return None
        
    headers = {
        "Authorization": f"Bearer {fortumToken}"
    }
    yesterday = str(getDate(-1 * days))
    today = str(getDate(0))
    
    # Format API params with environment variables
    formatted_params = apiParams.format(
        customer_id=fortumCustomerId,
        metering_point_no=fortumMeteringPointNo,
        metering_point_id=fortumMeteringPointId
    )
    
    path = f"{fortumApi}{formatted_params.replace('DATE_FROM',yesterday).replace('DATE_TO',today).replace('DATE_LATESTO',today)}"
    print (path)

    response = requests.get(path, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to fetch data:", response.status_code)
        return None

# Get consumption data for given number of days using datahub api
def getConsumptionDatahub(days = 1, token = None):
    if not meteringPoint:
        print("Error: Missing metering point EAN. Please check your environment variables.")
        return None
        
    deltaDay = (1 + days) * (-1)
    if debug:
        print (deltaDay)
    then = f"{str(getDate(deltaDay))}" #T22:00:00.000Z"
    now = f"{str(getDate(0))}" #T22:00:00.000Z"
    return getConsumptionHistory(then, now, token)

def getConsumptionHistory(then, now, filename = None, token = None, method='POST'):
    if not meteringPoint:
        print("Error: Missing metering point EAN. Please check your environment variables.")
        return None
        
    if not now:
        nowStr = then.split('T')[0]
        now = date.fromisoformat(nowStr) + timedelta(days=7)
        if debug:
            print('now', now)
    headers = {
        "Authorization": f"Bearer {token if token else datahubToken}"
    }

    thenUtc = getMidnightIsoFormat(then)
    nowUtc = getMidnightIsoFormat(now, lastMinute=True)

    if method == 'GET':
        path = f"{datahubApi}{datahubParams.format(metering_point_ean=meteringPoint).replace('DATE_FROM',thenUtc).replace('DATE_TO',nowUtc)}"
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
        response = readFromJson(filename)
        return response

    if response.status_code == 200:
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
    if debug:
        print ('url', url)

    # Making a GET request to the API
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the response JSON data
        data = response.json()
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
    else:
        nowUtc = getMidnightIsoFormat(now, lastMinute=True)
    
    print ('now', nowUtc)
    print ('now', now)
    url = f"{sahkotinApi}{thenUtc.replace(':00Z', ':00.000Z')}&end={nowUtc.replace(':00Z', ':00.000Z')}"
    print ('url', url)

    # Making a GET request to the API
    response = requests.get(url)
    if debug:
        print ('response', response)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the response JSON data
        data = response.json()
        return data
    else:
        print("Failed to fetch data:", response.status_code)
        return None

## Returns Date object delta days before or after today.
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

def getMidnightIsoFormat(dateStr, lastMinute=False):
    # If the string already contains timezone info, extract just the date part
    if isinstance(dateStr, str) and 'T' in dateStr:
        dateStr = dateStr.split('T')[0]
    
    midnight = '23:45:00' if lastMinute else '00:00:00'
    hourDiff = 3 if IS_SUMMER_TIME else 2
    tzinfo = '+03:00' if IS_SUMMER_TIME else '+02:00'
    localtimeStr = f"{dateStr}T{midnight}{tzinfo}"
    localTimeIso = datetime.fromisoformat(localtimeStr)
    utcTime = localTimeIso - timedelta(hours=hourDiff)
    return f"{utcTime}".replace(' ', 'T').replace(tzinfo, 'Z')

def toISOFormat(utcTime):
    dateStr = f"{utcTime}".replace(' ', 'T').split('+')[0]
    return f"{dateStr}Z"

def readFromJson(file='consumption.json'):
    if debug:
        print (f'Reading from file: {file}')
    try:
        with open(file, 'r') as file:
            return json.load(file)
    except:
        return None

# Disable debug
disable_debug()
