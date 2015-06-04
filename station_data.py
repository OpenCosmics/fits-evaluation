import urllib2
import json
from pprint import pprint

def extract_station_data(code):
    url = "http://data.hisparc.nl/api/station/%d/"%(code)
    try:
        response = json.loads(urllib2.urlopen(url).read())
    except urllib2.HTTPError:
        return None
    else:
        return response

def get_stations():
    data = []
    url = 'http://data.hisparc.nl/api/stations'
    response = json.loads(urllib2.urlopen(url).read())
    for station in response:
        data.append(station['number'])
    return data

def main():
    station_ids = get_stations()
    for code in station_ids:
        out = extract_station_data(code)
        if out is not None:
            pprint(out)

if __name__ == '__main__':
    main()
