#!/usr/bin/python3
# -*- coding: utf-8 -*-

import requests
import json


if __name__ == '__main__':
    # url = "http://35.200.55.101:3000/win/adv01"
    url = "http://0.0.0.0:3000/win/adv01"
    headers = {"Content-Type": "application/json"}

    obj = {"id": "123",
           "price": 1.1,
           "isClick": 1}
    json_data = json.dumps(obj).encode('utf-8')

    result = requests.post(url, json_data, headers=headers)
    print(result.text)
