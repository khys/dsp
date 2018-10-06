#!/usr/bin/python3
# -*- coding: utf-8 -*-

import requests
import json


if __name__ == '__main__':
    url = "http://35.201.94.38:80"  # lb
    # url = "http://35.221.95.73:3000"  # 1
    # url = "http://35.200.43.183:3000"  # 2
    # url = "http://35.221.105.45:3000"  # 3
    # url = "http://35.200.76.206:3000"  # 4
    # url = "http://35.200.100.17:3000"  # 5
    headers = {"Content-Type": "application/json"}

    obj = {"id": "123",
           "floorPrice": 100,
           "deviceId": "cc6f3c56-f35f-4de5-b6a0-6cf8f5fd44c2",
           "mediaId": "1000",
           "timestamp": 4567,
           "osType": "iOS",
           "bannerSize": 1,
           "bannerPosition": 1,
           "deviceType": 1}
    json_data = json.dumps(obj).encode('utf-8')

    result = requests.post(url, json_data, headers=headers)
    print(result.text)
