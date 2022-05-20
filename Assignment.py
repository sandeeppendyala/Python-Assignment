import time
import datetime
import json
import csv
from pytz import timezone
import xml.etree.ElementTree as ET


def get_date_with_added_interval(reviewinterval):
    dateformat = '%Y%m%d'
    current_date = time.strftime(dateformat)
    d = datetime.datetime.strptime(current_date, dateformat)
    new_date = d + datetime.timedelta(days=reviewinterval)
    sDateString = str(new_date.strftime(dateformat))
    return sDateString


def update_depart_and_return(x, y):
    past_date = get_date_with_added_interval(x*(-1))
    future_date = get_date_with_added_interval(y)
    tree = ET.parse('test_payload1.xml')
    root = tree.getroot()
    departtext = root.find('./REQUEST/TP/DEPART')
    returntext = root.find('./REQUEST/TP/RETURN')
    departdate = departtext.text = past_date
    returndate = returntext.text = future_date
    tree.write('test_payload1.xml')
    print(departdate)
    print(returndate)


def remove_elements_from_json(rootelm, nestedelm):
    with open('test_payload.json', 'r') as file:
        data = json.load(file)
        data.pop(rootelm)
    params = []
    for element in data['inParams']:
        params.append(element)
    params.remove(nestedelm)
    print(data)

    with open("test_payload.json", "w") as file:
        json.dump(data, file)


def parse_to_csv_and_verify():
    with open('Jmeter_log1.jtl', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if int(row['responseCode']) != 200:
                print(f"Non successful response received -> Label: {row['label']}, " +
                      f"Response Code: {row['responseCode']}, Response Message: {row['responseMessage']}, " +
                      f"Failure Message: {row['failureMessage']}, " +
                      f"Time: {datetime.datetime.fromtimestamp(float(int(row['timeStamp']) / 1000)).astimezone(timezone('US/Pacific')).strftime('%Y-%m-%d %H:%M:%S PST')} ");
                print("")


update_depart_and_return(2, 2)
remove_elements_from_json('outParams', 'appdate')
parse_to_csv_and_verify()
