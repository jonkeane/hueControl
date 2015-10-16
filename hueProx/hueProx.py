#! /usr/bin/python
import json, time, csv
import phue
from cgi import parse_qs, escape


def application(environ, start_response):
    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except (ValueError):
        request_body_size = 0

    queryD = parse_qs(environ['QUERY_STRING']) # escape to sanitize?
    data = {}
    for item in queryD.keys():
        data[item] = escape(queryD[item][0])
    f = open("/var/log/hueControl/hue_Proximity.csv", "a")
    data['time'] = time.ctime()
    w = csv.writer(f)
    w.writerow(data.values())
    f.close()

    f = open("/var/log/hueControl/hue_Proximity.log", "w")
    f.write(str(data))
    f.close()

    # Test for timing of arrivals.
    b = phue.Bridge('hueBridge')
    # If the app is not registered and the button is not pressed, press the button and call connect() (this only needs to be run a single time)
    b.connect()
    if data['state'] == '2' and float(data['devices']) >= 1 and float(data['devicesPrev']) <= 0 :
        b.set_light("Front door", 'on', True)
        b.set_light("Front door", 'bri', 254)
        b.set_light("Front door", 'sat', 0)


    start_response('200 OK', [('Content-Type', 'text/html')])
    return ["<h1>This should be sent to the router!</h1>"]
