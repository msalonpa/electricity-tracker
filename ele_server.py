from flask import Flask, jsonify, request
from flask_cors import CORS

from ele_api import * #getData, getConsumption, getSahkotinData, getConsumptionDatahub, getConsumptionHistory, getSahkotinHistory
from ele_parser import *

##
# Runs a REST API server in localhost port 5000
# Serves requests to fetch electricity prices and consumption data.
# Usage:
#  curl -X GET http://127.0.0.1:5000/data/now -H "Content-Type: application/json"
#  curl -X GET http://127.0.0.1:5000/consumption/2 -H "Content-Type: application/json"
##

app = Flask(__name__)
CORS(app) # This will enable CORS for all routes

# In-memory database for demonstration
data = [{"id": 1, "name": "Item 1"}]

@app.route('/data/<mode>', methods=['GET'])
def get_data(mode = 'now'):
    return get_data_format(mode, format=None)

@app.route('/data/<mode>/<format>', methods=['GET'])
def get_data_format(mode = 'now', format = 'list'):
    _data = getData(1 if mode == 'now' or mode == '1' else 2)
    if not _data:
        return {'Error': 500}

    k,v,p = parse_data(_data)
    if format == 'json':
        return jsonify(_data)
    return p

@app.route('/data', methods=['POST'])
def add_data():
    item = request.json
    data.append(item)
    return jsonify(item), 201

@app.route('/data', methods=['DELETE'])
def delete_data():
    data = []
    return {'Data cleared': 200}

@app.route('/days/<days>', methods=['GET'])
def get_dataDays(days = '1'):
    return get_dataDaysFormat(days = days, format = None)

@app.route('/days/<days>/<format>', methods=['GET'])
def get_dataDaysFormat(days = '1', format = None):
    _data = getSahkotinData(int(days))
    if not _data:
        return {'Error': 500}
    k,v,p = parse_prices_date_value(_data)
    return jsonify(_data) if format == 'json' else p

# Requires Fortum API key
@app.route('/consumption/<days>', methods=['GET'])
def get_consumption(days = '1'):
    _data = getConsumption(int(days))
    if _data:
        k,v,r = parse_consumption(_data)
        return r
        #return jsonify(_data)
    return {'Error': 500}

# Requires Fingrid Datahub API key
@app.route('/datahub/<days>', methods=['GET'])
def get_datahub(days = '1'):
    token = None
    if len(data) > 1:
        token = data[1]['token']

    _data = getConsumptionDatahub(int(days), token)
    if _data and 'ReasonCode' in _data:
        print ('DATA IS NOT VAIID')
        return _data['EventReasons']
    #print ('_data:')
    #print (_data)
    if _data:
        obs = parse_observations(_data)
        return {"results": obs}
    return {'Error': 500}

# Requires Fingrid Datahub API key
# Fetch consumption data using Fingrid API and price data using Sahkotin API
@app.route('/fulldata/<days>', methods=['GET'])
def get_fulldata(days = '1'):
    token = None
    if len(data) > 1:
        token = data[1]['token']

    ele_data = getSahkotinData(int(days))
    if not ele_data:
        return {'Error': 500, 'Reason': 'Price data not found'}

    #ct = {'TimeSeries': [{'MeteringPointEAN': '643007520004355712', 'ResolutionDuration': 'PT1H', 'PeriodStartTS': '2024-07-26T21:00:00Z', 'PeriodEndTS': '2024-07-28T21:00:00Z', 'ProductType': '8716867000030', 'UnitType': 'kWh', 'ReadingType': 'BN01', 'Observations': [{'Epoch': '1722027600000', 'PeriodStartTime': '2024-07-29T21:00:00Z', 'Quantity': '0.410000', 'Quality': 'OK'}, {'Epoch': '1722031200000', 'PeriodStartTime': '2024-07-29T22:00:00Z', 'Quantity': '0.650000', 'Quality': 'OK'}, {'Epoch': '1722034800000', 'PeriodStartTime': '2024-07-29T23:00:00Z', 'Quantity': '0.240000', 'Quality': 'OK'}, {'Epoch': '1722038400000', 'PeriodStartTime': '2024-07-30T00:00:00Z', 'Quantity': '0.510000', 'Quality': 'OK'}, {'Epoch': '1722042000000', 'PeriodStartTime': '2024-07-27T01:00:00Z', 'Quantity': '0.220000', 'Quality': 'OK'}]}]}
    #json, csv = create_price_table(ele_data, ct)
    #print (csv)
    
    cons_data = getConsumptionDatahub(int(days), token)
    if cons_data and 'ReasonCode' in cons_data:
        print ('DATA IS NOT VAIID')
        return cons_data['EventReasons']
    if not cons_data:
        return {'Error': 500, 'Reason': 'Consumption data not found'}

    json, csv, consumption, price = create_price_table(ele_data, cons_data)
    ppkwh = price / consumption

    return {"results": "In File", "price": price, "consumption": consumption, "ppkwh": f"{ppkwh:.3f} c/kwh"}
    #return {'Error': 500}

@app.route('/history/', methods=['GET'])
def get_history():
    fromDate = request.args.get('from', default=None)
    toDate = request.args.get('to', default=None)

    if not fromDate: # or not toDate:
        return {'Error': 404, "message": "Missing date parameter"}

    if not validateDate(fromDate): # or not validateDate(toDate):
        return {'Error': 404, "message": "Invalid date format"}

    #then = f"{fromDate}T00:00:00.000Z"
    #now = f"{toDate}T22:00:00.000Z" if toDate else None

    #print (f'Search Results for: {then}')
    #print (f'Search Results for: {now}')
    #return {'Error': 500}

    # TEST
    #_test = test_conversion(fromDate)
    #if not _test:
    #    return {'TEST OK': 200}
    token = None
    if len(data) > 1:
        token = data[1].token
    print (token)

    _data = getConsumptionHistory(fromDate, toDate)
    if _data and 'ReasonCode' in _data:
        print ('DATA IS NOT VAIID')
        return _data['EventReasons']
    #print ('_data:')
    #print (_data)
    if _data:
        obs = parse_observations(_data)
        return {"results": obs}
    return {'Error': 500}


@app.route('/pricehistory/', methods=['GET'])
def get_price_history():
    fromDate = request.args.get('from', default=None)
    toDate = request.args.get('to', default=None)

    if not fromDate or not toDate:
        return {'Error': 404, "message": "Missing date parameter"}

    if not validateDate(fromDate) or not validateDate(toDate):
        return {'Error': 404, "message": "Invalid date format"}

    then = f"{fromDate}T22:00:00.000Z"
    now = f"{toDate}T22:00:00.000Z" if toDate else None

    print (f'Search Results for: {fromDate} and {toDate}')
    print (f'Search Results for: {then} and {now}')
    #return {'Error': 500}

    _data = getSahkotinHistory(then, now)
    if _data:
        obs = parse_prices_date_value(_data)
        return {"results": obs}

    #print ('_data:')
    #print (_data)
    if _data:
        obs = parse_observations(_data)
        return {"results": obs}
    return {'Error': 500}

# Requires consumption data from consumption.json
# Returns winterday consumption and other time consumption
# Usage: curl -X GET http://127.0.0.1:5000/distribution/?month=12&year=2024
@app.route('/distribution/', methods=['GET'])
def get_distribution():
    month = request.args.get('month', default=None)
    year = request.args.get('year', default='25')
    print (f'consumption_{month}_{year}.json')
    if not month or not year:
        return {'Error': 404, "message":
                "Missing month or year parameter. Example: curl -X GET http://127.0.0.1:5000/distribution/?month=12&year=2024"}
    if len(month) != 2:
        month = f'0{month}'
    if len(year) > 2:
        year = year[2:]

    _data = readFromJson(f'data/consumption_{month}_{year}.json')

    if not _data:
        return {'Error': 404, "message": f"Consumption data for {month}/{year} not found"}

    winterdayConsumption, otherTimetConsumption = parse_consumption_distribution(_data)
    return {
        'month': month,
        'year': year,
        'winterdayConsumption': winterdayConsumption,
        'otherTimetConsumption': otherTimetConsumption,
        'totalConsumption': winterdayConsumption + otherTimetConsumption,
        'winterdayPercentage': winterdayConsumption / (winterdayConsumption + otherTimetConsumption) * 100,
    }

def validateDate(dateStr):
    ari = dateStr.split('-')
    if len(ari) == 3 and len(ari[0]) == 4:
        return True
    return False

if __name__ == '__main__':
    app.run(debug=True)
