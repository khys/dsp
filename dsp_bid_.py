#!/usr/bin/python3
# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify, json
import redis
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sklearn
from sklearn.decomposition import PCA
from sklearn import datasets
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import accuracy_score
from sklearn import cross_validation
import lightgbm as lgb
import pickle


app = Flask(__name__)

nurl_url = "http://35.200.55.101:3000/"
budget_dict = {}
r = redis.StrictRedis(host='10.0.0.3', port='6379', db=0)
adv_list = ["adv01",
            "adv02",
            "adv03",
            "adv04",
            "adv05",
            "adv06",
            "adv07",
            "adv08",
            "adv09",
            "adv10",
            "adv11",
            "adv12",
            "adv13",
            "adv14",
            "adv15",
            "adv16",
            "adv17",
            "adv18",
            "adv19",
            "adv20",
            ]
pklfile = "./easy_model.sav"
demografile = "./demogra.csv"
loaded_model = pickle.load(open(pklfile, 'rb'))
demogra = pd.read_csv(demografile)
advId_0 = [6, 12, 18]
advId_1 = [2, 11, 3, 16, 14, 20, 10]
advId_2 = [7, 15, 8, 5, 17, 4, 1, 9, 13, 19]


def pred_price(data_dict, user):
    data = pd.DataFrame([[data_dict['deviceId'], data_dict['bannerPosition'], data_dict['bannerSize'],
                          data_dict['deviceType'], data_dict['floorPrice'], data_dict['id'], data_dict['mediaId'],
                          data_dict['osType'], data_dict['timestamp'], adv_list.index(user) + 1]],
                        columns=['deviceId', 'bannerPosition', 'bannerSize', 'deviceType', 'floorPrice',
                                 'id', 'mediaId', 'osType', 'timestamp', 'advId'])

    dev_id = data_dict['deviceId']
    data['advId'] = data['advId'].replace(advId_0, 21).replace(advId_1, 22).replace(advId_2, 23)
    data['osType'] = data['osType'].replace('iOS', 0).replace('ANDROID', 1)
    data['gender'] = demogra[demogra['deviceId'] == dev_id]['gender'].replace('female', 0).replace('male', 1).replace('UNKNOWN', 2)
    data['isMarried'] = demogra[demogra['deviceId'] == dev_id]['isMarried'].replace('yes', 0).replace('no', 1)

    x_test = pd.concat([data['bannerSize'], data['bannerPosition'], data['floorPrice'], data['osType'],
                        data['advId'], data['gender'], data['isMarried']], axis=1)
    cpc = float(r.hget(user, 'cpc').decode('utf-8'))
    ctr = loaded_model.predict(x_test, n_jobs=1)[0]
    price = cpc * ctr * 1000

    return price


@app.route('/', methods=['POST'])
def dsp_bid():
    data_r = request.data.decode('utf-8')
    data_dict = json.loads(data_r)
    data_dict['floorPrice'] = float(data_dict['floorPrice'])
    data_dict['timestamp'] = int(data_dict['timestamp'])
    data_dict['bannerSize'] = int(data_dict['bannerSize'])
    data_dict['bannerPosition'] = int(data_dict['bannerPosition'])
    if 'deviceType' in data_dict.keys():
        data_dict['deviceType'] = int(data_dict['deviceType'])
    else:
        data_dict['deviceType'] = int(data_dict['deviceToken'])
        data_dict.pop('deviceToken')

    budget_dict = {}
    for user in adv_list:
        budget_dict[user] = r.hget(user, 'budget')
    price = pred_price(data_dict, "adv01")
    if price == -1:
        return '', 204
    else:
        response = jsonify({
            "id": data_dict['id'],
            "bidPrice": price,
            "advertiserId": "adv01",
            "nurl": nurl_url + "win/adv01"})
        response.status_code = 200
        return response


if __name__ == '__main__':
    app.run()
