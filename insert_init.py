#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''insert budget data to redis
'''

import redis
import json


if __name__ == '__main__':
    r = redis.StrictRedis(host='10.0.0.3', port='6379', db=0)
    budget_f = open("./cpc_budget.json")
    budget_dict = json.load(budget_f)
    for key, value in budget_dict.items():
        r.hmset(key, value)
    print(r.hget('adv01', 'budget'))

    r1 = redis.StrictRedis(host='10.0.0.3', port='6379', db=1)
    for key, value in budget_dict.items():
        r1.hmset(key, value)
    print(r1.hget('adv01', 'budget'))
    r2 = redis.StrictRedis(host='10.0.0.3', port='6379', db=2)
    r2.set("b_n", 1)
    r2.set("c", 1)
    r2.set("ctr", 1)
