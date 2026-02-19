import json
from datetime import datetime
import pytz
import csv
import xlsxwriter
from models import PriceData

def enable_debug():
    global debug
    debug = True

def disable_debug():
    global debug
    debug = False

def test_parse():
    # JSON string
    json_string = '''
    [
        {"name": "Alice", "age": 30, "city": "New York"},
        {"name": "Bob", "age": 25, "city": "Los Angeles"},
        {"name": "Charlie", "age": 35, "city": "Chicago"}
    ]
    '''
    data = parse_person_data(json_string)
    print (data)

def test_conversion(dateStr):
    return convertDateToIsoTime(dateStr)


def parse_person_data(json_string):
    # Parsing the JSON string into a Python object
    data = json.loads(json_string)

    # Now `data` is a Python list of dictionaries
    for person in data:
        print(f"Name: {person['name']}, Age: {person['age']}, City: {person['city']}")

    return 1

def convertDateToIsoTime(dateStr):
    if debug:
        print (dateStr)
    local_time = f"{dateStr}T00:00:000+03:00"
    utcTime = datetime.fromisoformat(local_time).astimezone(pytz.timezone('Europe/London'))
    #return f"{utcTime}".replace(' ', 'T').replace(tzinfo, 'Z')
    if debug:
        print (utcTime)

def parse_data(json_string):
    # Parsing the JSON string into a Python object
    try:
        data = json.loads(json_string)
    except:
        data = json_string

    # Use the data model
    price_data = PriceData.from_dict({'hour': data.get('hour', [])})
    return price_data

def parse_prices_date_value(json_string):
    # Parsing the JSON string into a Python object
    try:
        data = json.loads(json_string)['prices']
    except:
        data = json_string['prices']
    if debug:
        print (data)

    keys = []
    values = []
    prices = []

    if debug:
        print (f"Hinnat {data[0]['date']}")
    #print (data.values)

    # Now `data` is a Python list of dictionaries
    for price in data:
        keys.append(price['date'])
        values.append(price['value'])
        local_time = datetime.fromisoformat(price['date'].replace('Z', '+00:00')).astimezone(pytz.timezone('Europe/Helsinki'))
        formatted_time = local_time.strftime('%Y-%m-%d %H:%M:%S')
        prices.append(f"{formatted_time} - Value: {price['value']}")

    return (keys, values, prices)

def parse_consumption(json_string):
    # Parsing the JSON string into a Python object
    try:
        data = json.loads(json_string)
    except:
        data = json_string

    keys = []
    values = []
    result = []

    if not data['consumption']:
        print (f"\nKulutustiedot puuttuu")
    else:
        print (f"\nKulutus {data['consumption'][0]['fromTime']}")

        # Now `data` is a Python list of dictionaries
        for consumption in data['consumption']:
            keys.append(consumption['fromTime'])
            values.append(consumption['energy'])
            formatted_time = consumption['fromTime'].replace('T', ' ')
            result.append(f"{formatted_time} - Quantity: {consumption['energy']}")
            if debug:
                print(consumption['energy'])

    return (keys, values, result)

def parse_observations(data):
    if not 'TimeSeries' in data:
        return []

    observations = data['TimeSeries'][0]['Observations']
    result = []

    for obs in observations:
        if obs['Quality'] == 'OK':
            # Convert the UTC time to local time. Adjust 'Europe/Helsinki' as per your local timezone
            local_time = datetime.fromisoformat(obs['PeriodStartTime'].replace('Z', '+00:00')).astimezone(pytz.timezone('Europe/Helsinki'))
            formatted_time = local_time.strftime('%Y-%m-%d %H:%M:%S')
            result.append(f"{formatted_time} - Quantity: {obs['Quantity']}")

    return result

def create_price_table(priceData, consumptionData):
    # Parsing the JSON string into a Python object
    try:
        prices = json.loads(priceData)['prices']
    except:
        prices = priceData['prices']

    if not 'TimeSeries' in consumptionData:
        return []

    observations = consumptionData['TimeSeries'][0]['Observations']
    periodStart = None

    #titles = ['Time,Price,Margin,Total Price,Quantity,Total']
    titles = ['Time','Price','Margin','Totalprice','Consumption','Total','Daily Cons','Daily Price','Daily Avg']
    rows = []
    result = []
    margin = 0.6
    total_consumption = 0
    total_price = 0
    daily_total = 0
    daily_cons = 0

    for price in prices:
        local_time = datetime.fromisoformat(price['date'].replace('Z', '+00:00')).astimezone(pytz.timezone('Europe/Helsinki'))
        formatted_time = local_time.strftime('%Y-%m-%d %H:%M:%S')
        if periodStart is None:
            periodStart = formatted_time.split(' ')[0]
        hourprice = float(price['value'])
        totalprice = hourprice + margin
        row = {"Time": formatted_time}
        #row['Margin'] = margin.replace('.',',')
        row['Price'] = f'{hourprice:.3f}'.replace('.',',')
        row['Margin'] = f'{margin:.2f}'.replace('.',',')
        row['Totalprice'] = f'{totalprice:.3f}'.replace('.',',')
        #row['Totalprice'] = totalprice
        for obs in observations:
            if obs['Quality'] == 'OK':
                if price['date'].replace('.000Z', 'Z') == obs['PeriodStartTime']:
                    quantity = float(obs['Quantity'])
                    total = totalprice * quantity
                    total_consumption += quantity
                    total_price += total
                    daily_cons += quantity
                    daily_total += total
                    row['Consumption'] = f'{quantity:.3f}'.replace('.',',')
                    row['Total'] = f'{total:.3f}'.replace('.',',')
                    if (local_time.strftime("%H") == '23'):
                        daily_avg = daily_total / daily_cons
                        row['Daily Cons'] = f'{daily_cons:.3f}'.replace('.',',')
                        row['Daily Price'] = f'{(daily_total / 100):.3f}'.replace('.',',')
                        row['Daily Avg'] = f'{daily_avg:.3f}'.replace('.',',')
                        daily_total = 0
                        daily_cons = 0
                    rows.append(f"{formatted_time},{row['Price']},{margin},{totalprice},{obs['Quantity']},{total}")
                    break
        result.append(row)

    #print (f"Hinnat json: {result}")
    createExcelFile(result, f"records/record_{periodStart}.xlsx")

    with open(f'records/record_{periodStart}.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=titles)
        writer.writeheader()
        writer.writerows(result)
    return (result, '\n\r'.join(rows), total_consumption, total_price)

def createExcelFile(consumptionData, filename='records.xlsx'):
    workbook = xlsxwriter.Workbook(filename)
    worksheet = workbook.add_worksheet()

    # Write headers
    titles = ['Time', 'Price', 'Margin', 'Totalprice', 'Consumption', 'Total', 'Daily Cons', 'Daily Price', 'Daily Avg']
    for col, title in enumerate(titles):
        worksheet.write(0, col, title)

    # Write data rows
    for row_idx, data in enumerate(consumptionData, start=1):
        worksheet.write(row_idx, 0, data.get('Time', ''))
        worksheet.write(row_idx, 1, float(data.get('Price', '0').replace(',', '.')))
        worksheet.write(row_idx, 2, float(data.get('Margin', '0').replace(',', '.')))
        worksheet.write(row_idx, 3, float(data.get('Totalprice', '0').replace(',', '.')))
        worksheet.write(row_idx, 4, float(data.get('Consumption', '0').replace(',', '.')))
        worksheet.write(row_idx, 5, float(data.get('Total', '0').replace(',', '.')))
        worksheet.write(row_idx, 6, float(data.get('Daily Cons', '0').replace(',', '.')) if 'Daily Cons' in data else '')
        worksheet.write(row_idx, 7, float(data.get('Daily Price', '0').replace(',', '.')) if 'Daily Price' in data else '')
        worksheet.write(row_idx, 8, float(data.get('Daily Avg', '0').replace(',', '.')) if 'Daily Avg' in data else '')

    workbook.close()

def parse_consumption_distribution(data):
    if not 'TimeSeries' in data:
        return []

    observations = data['TimeSeries'][0]['Observations']
    winterdayConsumption = 0
    otherTimetConsumption = 0

    for obs in observations:
        if obs['Quality'] == 'OK':
            # Convert the UTC time to local time. Adjust 'Europe/Helsinki' as per your local timezone
            local_time = datetime.fromisoformat(obs['PeriodStartTime'].replace('Z', '+00:00')).astimezone(pytz.timezone('Europe/Helsinki'))

            if local_time.month >= 4 and local_time.month < 11:
                otherTimetConsumption += float(obs['Quantity'])
            else:
                if local_time.weekday() < 6 and local_time.hour >= 7 and local_time.hour < 22:
                    winterdayConsumption += float(obs['Quantity'])
                else:
                    otherTimetConsumption += float(obs['Quantity'])
    
    return (winterdayConsumption, otherTimetConsumption)

def parse_consumption_distribution_json(data):
    return parse_consumption_distribution(json.loads(data))

# Disable debug
disable_debug()
