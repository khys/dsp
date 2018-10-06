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
r1 = redis.StrictRedis(host='10.0.0.3', port='6379', db=1)
r2 = redis.StrictRedis(host='10.0.0.3', port='6379', db=2)
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
pklfile = './Lgb_.sav'
demografile = "./demogra.csv"
media_file = './mediaId_listfile'
loaded_model = pickle.load(open(pklfile, 'rb'))
list_ = pickle.load(open(media_file, 'rb'))
demogra = pd.read_csv(demografile)
advId_0 = [6, 12, 18]
advId_1 = [2, 11, 3, 16, 14, 20, 10]
advId_2 = [7, 15, 8, 5, 17, 4, 1, 9, 13, 19]
listA = list(list_.index)[0:331]
listB = list(list_.index)[332:661]
listC = list(list_.index)[662:1000]


def pred_ctr(data_dict):
    data = pd.DataFrame([[data_dict['deviceId'], data_dict['bannerPosition'], data_dict['bannerSize'],
                          data_dict['deviceType'], data_dict['floorPrice'], data_dict['id'], data_dict['mediaId'],
                          data_dict['osType'], data_dict['timestamp']]],
                        columns=['deviceId', 'bannerPosition', 'bannerSize', 'deviceType', 'floorPrice',
                                 'id', 'mediaId', 'osType', 'timestamp'])

    dev_id = data_dict['deviceId']
    demogra_dev = demogra[demogra['deviceId'] == dev_id]
    data['osType'] = data['osType'].replace('iOS', 0).replace('ANDROID', 1)
    data['gender'] = demogra_dev['gender'].replace('female', 0).replace('male', 1).replace(
        'UNKNOWN', 2)
    data['isMarried'] = demogra_dev['isMarried'].replace('yes', 0).replace('no', 1)
    data['age'] = demogra_dev['age']
    data['income'] = demogra_dev['income']
    data['mediaId'] = data['mediaId'].replace(listA, 1001).replace(listB, 1002).replace(listC, 1003)
    hour = pd.to_datetime(data['timestamp'], unit='s').dt.hour
    dayofweek = pd.to_datetime(data['timestamp'], unit='s').dt.dayofweek

    x_test = pd.concat([data['bannerSize'], data['bannerPosition'], data['floorPrice'] / 1000, data['mediaId'],
                        data['osType'], data['gender'], data['isMarried'], (data['age'].fillna(0) / 10).astype(int),
                        (data['income'].fillna(0) / 100).astype(int), hour, dayofweek], axis=1)
    ctr = loaded_model.predict(x_test, n_jobs=1)[0]

    return ctr


def return_ctr():
    return 0.6


@app.route('/', methods=['POST'])
def dsp_bid():
    data_r = request.data.decode('utf-8')
    data_dict = json.loads(data_r)
    data_dict['floorPrice'] = float(data_dict['floorPrice'])
    data_dict['timestamp'] = int(data_dict['timestamp'])
    data_dict['bannerSize'] = int(data_dict['bannerSize'])
    data_dict['bannerPosition'] = int(data_dict['bannerPosition'])
    data_dict['mediaId'] = int(data_dict['mediaId'])
    if 'deviceType' in data_dict.keys():
        data_dict['deviceType'] = int(data_dict['deviceType'])
    else:
        data_dict['deviceType'] = int(data_dict['deviceToken'])
        data_dict.pop('deviceToken')

    budget_dict = {}
    for user in adv_list:
        budget_dict[user] = r.hget(user, 'budget')
    adv_n = {}
    b_n = int(r2.get("b_n").decode('utf-8'))
    c = int(r2.get("c").decode('utf-8'))
    # ctr = return_ctr()
    ctr = pred_ctr(data_dict)
    for user in adv_list:
        cpc = float(r.hget(user, 'cpc').decode('utf-8'))
        if float(budget_dict[user]) <= 100:
            a_n = 0
        else:
            # a_n = 1
            a_n = float(r.hget(user, 'budget').decode('utf-8')) / float(r1.hget(user, 'budget').decode('utf-8'))
        adv_n[user] = cpc * ctr * a_n * b_n * c * 1000
    price = int(max(adv_n.values()))
    inverse = [(value, key) for key, value in adv_n.items()]
    user = max(inverse)[1]

    if price < data_dict['floorPrice'] + 1:
        return '', 204
    response = jsonify({
        "id": data_dict['id'],
        "bidPrice": price,
        "advertiserId": user,
        "nurl": nurl_url + "win/" + str(user)})
    response.status_code = 200
    return response


if __name__ == '__main__':
    app.run()
