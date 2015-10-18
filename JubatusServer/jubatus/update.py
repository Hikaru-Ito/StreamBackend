#!/usr/bin/env python
# -*- coding:utf-8 -*-

host = '127.0.0.1'
port = 9199
name = 'dmp'

import jubatus
from jubatus.common import Datum

import json

LEARNING_JSON_PATH = './data/data-5000.json'


def connect_jubatus():
    client = jubatus.Recommender(host, port, name)
    return client


def update(learning_json_path):
    client = connect_jubatus()
    with open(learning_json_path) as f:
        learning_data = json.load(f)
        print(json.dumps(learning_data, sort_keys=True, indent=4))
    for value in learning_data:
        d = Datum(value)
        client.update_row(value['id'],d)
        print value['title']

def main():
    update(LEARNING_JSON_PATH)

if __name__ == '__main__':
    main()
