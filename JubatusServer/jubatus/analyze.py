#!/usr/bin/env python
# -*- coding: utf-8 -*-

host = '127.0.0.1'
port = 9199
name = 'dmp'

import jubatus
from jubatus.common import Datum

import json

TARGET_JSON_PATH = './documents.json'


def connect_jubatus():
    client = jubatus.Recommender(host, port, name)
    return client


def analyze(target_json_path):
    client = connect_jubatus()
    with open(target_json_path) as f:
        target_data = json.load(f)
        print target_data
        # for value in target_data:
            # print value['title']
    d = Datum(target_data)
    print d
    sr = client.similar_row_from_datum(d, 100)
    return sr


def main():
    sr = analyze(TARGET_JSON_PATH)
    for r in sr:
        print r.id, "with score", r.score

if __name__ == '__main__':
    main()
