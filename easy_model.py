#!/usr/bin/python3

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
import time

pklfile = "./easy_model.sav"
demografile = "./demogra.csv"
loaded_model = pickle.load(open(pklfile, 'rb'))
demogra = pd.read_csv(demografile)

advId_0 = [6, 12, 18]
advId_1 = [2, 11, 3, 16, 14, 20, 10]
advId_2 = [7, 15, 8, 5, 17, 4, 1, 9, 13, 19]

start = time.time()

data = pd.DataFrame([['cc6f3c56-f35f-4de5-b6a0-6cf8f5fd44c2', 6, 4, 1, 19392.0,
                      '8abefa99-20b6-45ea-8e5b-c74081fb1fb1', 608, 'iOS', 1535203765, 11, 0]],
                    columns=['deviceId', 'bannerPosition', 'bannerSize', 'deviceType', 'floorPrice',
                             'id', 'mediaId', 'osType', 'timestamp', 'advId', 'isClick'])
merge = pd.merge(demogra, data, on='deviceId')

merge['advId'] = merge['advId'].replace(advId_0, 21).replace(advId_1, 22).replace(advId_2, 23)
merge['osType'] = merge['osType'].replace('iOS', 0).replace('ANDROID', 1)
merge['gender'] = merge['gender'].replace('female', 0).replace('male', 1).replace('UNKNOWN', 2)
merge['isMarried'] = merge['isMarried'].replace('yes', 0).replace('no', 1)

X_test = pd.concat([merge['bannerSize'], merge['bannerPosition'], merge['floorPrice'], merge['osType'],
                    merge['advId'], merge['gender'], merge['isMarried']], axis=1)
result = loaded_model.predict(X_test)

elapsed_time = time.time() - start
print("{0} sec ({1})".format(elapsed_time, result))
