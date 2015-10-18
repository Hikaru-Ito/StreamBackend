#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Jubatus Server Host
host = '127.0.0.1'
port = 9199
name = 'dmp'

# Import Libraries
import jubatus
from jubatus.common import Datum

import json

from bottle import route, run, template, HTTPResponse, request

# Jubatus Recommender Function
def connect_jubatus():
    client = jubatus.Recommender(host, port, name)
    return client


def analyze(obj):
    client = connect_jubatus()
    d = Datum(obj)
    sr = client.similar_row_from_datum(d, 100)
    return sr

# HTTP Request API
@route('/api/recommender', method='GET')
def index():
    textdata = request.query.textdata
    print textdata
    data = { "title": textdata }
    sr = analyze(data)
    dictionary = []
    for r in sr:
        dictionary_data = {
            "posts_id":r.id,
            "score":r.score
        }
        dictionary.append(dictionary_data)
        print r.id, "with score", r.score
    body = json.dumps(dictionary)
    r = HTTPResponse(status=200, body=body)
    r.set_header('Content-Type', 'application/json')
    return r

run(host='127.0.0.1', port=8030, debug=True, reloader=True)
