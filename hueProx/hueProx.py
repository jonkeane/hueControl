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
    f = open("./dash_Proximity.csv", "a")
    data['time'] = time.ctime()
    w = csv.writer(f)
    w.writerow(data.values())
    f.close()


    start_response('200 OK', [('Content-Type', 'text/html')])
    return ["<h1>This should be sent to the router!</h1>"]
