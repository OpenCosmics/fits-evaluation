from datetime import date, datetime
from urllib import urlencode
#from pylab import plot, show
import urllib2
import json
from pprint import pprint
from StringIO import StringIO
from numpy import genfromtxt
import csv

def get_station_data(code):
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


def get_events(station, start, end):
    """
    Event Summary Data
    ------------------
    date:                time of event [GPS calendar date]
    time:                time of event [GPS time of day]
    timestamp:           time of event [UNIX timestamp]
    nanoseconds:         time of event [number of nanoseconds after timestamp]
    pulseheights (4x):   maximum signal pulseheight [ADC]
    integral (4x):       integral of the signal [ADC.ns]
    number_of_mips (4x): estimate for the number of particles in the detector
    arrival_times (4x):  relative time of arrival of the first particle in the
                         detector [ns]
    trigger_time:        relative time of the trigger timestamp [ns]

    Values of -1 for detectors 3 and 4 indicate that the station only has
    two detectors.  Values of -999 indicate a problem in the analysis of
    that particular event.  This may be the result from noise in the signal.
    """

    event = {}
    event_list = []
    url = 'http://data.hisparc.nl/data/'+str(station)+'/events'
    query = urlencode({'download': False, 'start': start,'end': end})

    # Read the string as a file object
    data = StringIO(urllib2.urlopen(url + '?' + query).read())

    # Read the station data
    station_data = get_station_data(station)

    csv_obj = csv.reader(data, delimiter = '\t')
    for row in csv_obj:
        # Ignore rows starting with a # (comments)
        if row[0].startswith('#'):
            continue

        # Do NOT convert date and time to Python formats as they are not JSON
        # serializable

        event['location'] = {
                             'latitude'  : station_data['latitude'],
                             'longitude' : station_data['longitude'],
                             'altitude'  : station_data['altitude']
                            }

        event['time'] = row[0] + ' ' + row[1] + '%9d'%(int(row[2]))

        event['window'] = None

        event['livetime'] = None

        event['UID'] = station_data['number']

        event['status'] = 'active' if bool(station_data['active']) else 'inactive'

        event['measurement'] = {
                                'pulseheights'  : [int(row[4]), int(row[5]),
                                                   int(row[6]), int(row[7])],

                                'integral'      : [int(row[8]), int(row[9]),
                                                   int(row[10]), int(row[11])],

                                'number_of_mips': [float(row[12]), float(row[13]),
                                                   float(row[14]), float(row[15])],

                                'arrival_times' : [float(row[16]), float(row[17]),
                                                   float(row[18]), float(row[19])],
                                'trigger_time'  : float(row[20])
                               }

        event_list.append(event)

    return event_list

def main():
    station_id = 3
    events = get_events(station_id, datetime(2013, 7, 2, 11, 0),
                                    datetime(2013, 7, 2, 11, 05))

    # Event output as Python dictionary
    # pprint(events)

    # Generate a JSON dump
    print(json.dumps(events, sort_keys=True, indent=4))


if __name__ == '__main__':
    main()
